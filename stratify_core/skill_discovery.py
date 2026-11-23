"""
STRATIFY Skill Discovery Engine
Discovers and inspects available AI agent skills, installed skills, and SKILL.md files.
Strictly verifies actual skill availability on disk to prevent inventing non-existent skills.
"""
import os
import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SkillMetadata(BaseModel):
    id: str
    name: str
    category: str
    description: str
    industry_affinity: List[str] = Field(default_factory=list)
    token_weight: int = 750
    file_path: str
    is_available: bool = True

class SkillDiscovery:
    def __init__(self, skills_dir: Optional[str] = None):
        if skills_dir is None:
            # Default to project root / skills
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.skills_dir = os.path.abspath(os.path.join(current_dir, "..", "skills"))
        else:
            self.skills_dir = os.path.abspath(skills_dir)
        self._cached_skills: Optional[Dict[str, SkillMetadata]] = None

    def discover_skills(self, force_refresh: bool = False) -> Dict[str, SkillMetadata]:
        if self._cached_skills is not None and not force_refresh:
            return self._cached_skills

        discovered: Dict[str, SkillMetadata] = {}

        if not os.path.exists(self.skills_dir):
            return discovered

        for item in os.listdir(self.skills_dir):
            item_path = os.path.join(self.skills_dir, item)
            skill_md_path = os.path.join(item_path, "SKILL.md")
            
            if os.path.isdir(item_path) and os.path.exists(skill_md_path):
                meta = self._parse_skill_file(skill_md_path, fallback_id=item)
                if meta:
                    discovered[meta.id] = meta

        self._cached_skills = discovered
        return discovered

    def get_skill(self, skill_id: str) -> Optional[SkillMetadata]:
        skills = self.discover_skills()
        return skills.get(skill_id)

    def load_skill_instructions(self, skill_id: str) -> Optional[str]:
        skill = self.get_skill(skill_id)
        if not skill or not os.path.exists(skill.file_path):
            return None
        with open(skill.file_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Strip frontmatter
        clean_content = re.sub(r'^---[\s\S]*?---\s*', '', content)
        return clean_content.strip()

    def _parse_skill_file(self, file_path: str, fallback_id: str) -> Optional[SkillMetadata]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            name = fallback_id.replace("-", " ").title()
            skill_id = fallback_id
            category = "General"
            description = ""
            affinities = ["all"]
            token_weight = 750

            fm_match = re.search(r'^---([\s\S]*?)---', content)
            if fm_match:
                fm_text = fm_match.group(1)
                for line in fm_text.splitlines():
                    line = line.strip()
                    if line.startswith("name:"):
                        name = line.split(":", 1)[1].strip().strip('"').strip("'")
                    elif line.startswith("id:"):
                        skill_id = line.split(":", 1)[1].strip().strip('"').strip("'")
                    elif line.startswith("category:"):
                        category = line.split(":", 1)[1].strip().strip('"').strip("'")
                    elif line.startswith("description:"):
                        description = line.split(":", 1)[1].strip().strip('"').strip("'")
                    elif line.startswith("token_weight:"):
                        try:
                            token_weight = int(line.split(":", 1)[1].strip())
                        except ValueError:
                            pass
                    elif line.startswith("industry_affinity:"):
                        raw_aff = line.split(":", 1)[1].strip()
                        raw_aff = raw_aff.strip("[]").replace("'", "").replace('"', "")
                        affinities = [a.strip() for a in raw_aff.split(",") if a.strip()]

            return SkillMetadata(
                id=skill_id,
                name=name,
                category=category,
                description=description,
                industry_affinity=affinities,
                token_weight=token_weight,
                file_path=file_path,
                is_available=True
            )
        except Exception as e:
            print(f"Error parsing skill at {file_path}: {e}")
            return None
