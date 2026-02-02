"""Stack detection engine for Rulesmith."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from cli.src.config.schema import StackResult


class StackDetector:
    """Detects technology stack from project files."""

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)

    def detect(self) -> StackResult:
        """Detect technology stack from project files."""
        signals = self._collect_signals(self.project_path)
        return self._match_stack(signals)

    def _collect_signals(self, path: Path) -> Dict[str, Any]:
        """Scan for all detection signals."""
        signals = {}

        # JavaScript/Node signals
        package_json_path = path / "package.json"
        if package_json_path.exists():
            signals["package_json"] = self._parse_package_json(package_json_path)

        # Python signals
        requirements_path = path / "requirements.txt"
        if requirements_path.exists():
            signals["requirements"] = self._parse_requirements(requirements_path)

        pyproject_path = path / "pyproject.toml"
        if pyproject_path.exists():
            signals["pyproject"] = self._parse_pyproject(pyproject_path)

        # Rust signals
        cargo_path = path / "Cargo.toml"
        if cargo_path.exists():
            signals["cargo"] = self._parse_cargo(cargo_path)

        # Go signals
        gomod_path = path / "go.mod"
        if gomod_path.exists():
            signals["go_mod"] = self._parse_go_mod(gomod_path)

        # Ruby signals
        gemfile_path = path / "Gemfile"
        if gemfile_path.exists():
            signals["gemfile"] = True

        # PHP signals
        composer_path = path / "composer.json"
        if composer_path.exists():
            signals["composer"] = self._parse_composer(composer_path)

        # .NET signals
        csproj_files = list(path.glob("**/*.csproj"))
        if csproj_files:
            signals["csproj"] = len(csproj_files)

        # Flutter/Dart signals
        pubspec_path = path / "pubspec.yaml"
        if pubspec_path.exists():
            signals["pubspec"] = self._parse_pubspec(pubspec_path)

        # Java signals
        if (path / "pom.xml").exists():
            signals["maven"] = True
        if (path / "build.gradle").exists():
            signals["gradle"] = True

        return signals

    def _parse_package_json(self, path: Path) -> Dict[str, Any]:
        """Parse package.json file."""
        try:
            with open(path) as f:
                data = json.load(f)
            return {
                "dependencies": list(data.get("dependencies", {}).keys()),
                "devDependencies": list(data.get("devDependencies", {}).keys()),
                "scripts": list(data.get("scripts", {}).keys()),
            }
        except Exception:
            return {}

    def _parse_requirements(self, path: Path) -> List[str]:
        """Parse requirements.txt file."""
        try:
            with open(path) as f:
                lines = f.readlines()
            # Extract package names (handle comments and versions)
            packages = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    # Remove version specifiers
                    package = re.split(r"[<>=!~]", line)[0].strip()
                    if package:
                        packages.append(package)
            return packages
        except Exception:
            return []

    def _parse_pyproject(self, path: Path) -> Dict[str, Any]:
        """Parse pyproject.toml file."""
        try:
            import tomllib

            with open(path, "rb") as f:
                data = tomllib.load(f)

            result = {}
            if "project" in data:
                result["name"] = data["project"].get("name")
                result["dependencies"] = data["project"].get("dependencies", [])
            if "tool" in data:
                if "poetry" in data["tool"]:
                    result["tool"] = "poetry"
                elif "rye" in data["tool"]:
                    result["tool"] = "rye"
            return result
        except Exception:
            return {}

    def _parse_cargo(self, path: Path) -> Dict[str, Any]:
        """Parse Cargo.toml file."""
        try:
            import tomllib

            with open(path, "rb") as f:
                data = tomllib.load(f)

            return {
                "name": data.get("package", {}).get("name"),
                "dependencies": list(data.get("dependencies", {}).keys()),
            }
        except Exception:
            return {}

    def _parse_go_mod(self, path: Path) -> Dict[str, Any]:
        """Parse go.mod file."""
        try:
            with open(path) as f:
                content = f.read()

            # Extract module name and Go version
            module_match = re.search(r"^module\s+(\S+)", content, re.MULTILINE)
            go_version_match = re.search(r"^go\s+(\S+)", content, re.MULTILINE)

            return {
                "module": module_match.group(1) if module_match else None,
                "go_version": go_version_match.group(1) if go_version_match else None,
            }
        except Exception:
            return {}

    def _parse_composer(self, path: Path) -> Dict[str, Any]:
        """Parse composer.json file."""
        try:
            with open(path) as f:
                data = json.load(f)
            return {
                "name": data.get("name"),
                "dependencies": list(data.get("require", {}).keys()),
            }
        except Exception:
            return {}

    def _parse_pubspec(self, path: Path) -> Dict[str, Any]:
        """Parse pubspec.yaml file."""
        try:
            import yaml

            with open(path) as f:
                data = yaml.safe_load(f)

            return {
                "name": data.get("name"),
                "dependencies": list(data.get("dependencies", {}).keys()),
            }
        except Exception:
            return {}

    def _match_stack(self, signals: Dict[str, Any]) -> StackResult:
        """Match collected signals to known stacks."""
        scores: Dict[str, float] = {}

        # Helper functions for checking dependencies
        def has_package_json_dep(dep: str) -> bool:
            deps = signals.get("package_json", {}).get("dependencies", [])
            return dep in deps

        def has_requirement(pkg: str) -> bool:
            reqs = signals.get("requirements", [])
            return pkg in reqs

        def has_pyproject_dep(dep: str) -> bool:
            deps = signals.get("pyproject", {}).get("dependencies", [])
            return any(dep in d for d in deps)

        # Next.js Full-Stack detection
        if has_package_json_dep("next"):
            scores["nextjs-fullstack"] = 100
        elif has_package_json_dep("react"):
            # Check for backend indicators
            if (
                has_package_json_dep("express")
                or has_package_json_dep("fastify")
                or has_package_json_dep("koa")
            ):
                scores["express-react"] = 80
            else:
                scores["react-spa"] = 70

        # Django detection
        if has_requirement("django") or has_pyproject_dep("django"):
            if has_package_json_dep("react"):
                scores["django-react"] = 90
            else:
                scores["django"] = 85

        # FastAPI detection
        if has_requirement("fastapi") or has_pyproject_dep("fastapi"):
            if has_package_json_dep("vue"):
                scores["fastapi-vue"] = 90
            else:
                scores["fastapi"] = 85

        # Flask detection
        if has_requirement("flask") or has_pyproject_dep("flask"):
            scores["flask"] = 80

        # Laravel detection
        if signals.get("composer", {}).get("dependencies", []):
            deps = signals["composer"]["dependencies"]
            if "laravel/framework" in deps:
                scores["laravel"] = 100
            elif "symfony/framework-bundle" in deps:
                scores["symfony"] = 90

        # Rails detection
        if signals.get("gemfile"):
            scores["rails"] = 90

        # Rust detection
        if signals.get("cargo"):
            cargo_deps = signals["cargo"].get("dependencies", [])
            if "actix-web" in cargo_deps:
                scores["rust-actix"] = 95
            elif "rocket" in cargo_deps:
                scores["rust-rocket"] = 95
            elif "axum" in cargo_deps:
                scores["rust-axum"] = 95
            else:
                scores["rust"] = 80

        # Go detection
        if signals.get("go_mod"):
            scores["go"] = 80

        # Flutter detection
        if signals.get("pubspec"):
            scores["flutter"] = 90

        # Python Data/ML detection
        data_ml_packages = ["pandas", "numpy", "scikit-learn", "jupyter", "matplotlib"]
        if any(has_requirement(pkg) for pkg in data_ml_packages):
            scores["python-data-ml"] = 85

        # NestJS detection
        if has_package_json_dep("@nestjs/core"):
            scores["nestjs"] = 95

        # Determine primary stack
        if scores:
            primary = max(scores, key=scores.get)
            confidence = scores[primary] / 100
        else:
            primary = "unknown"
            confidence = 0.0

        return StackResult(
            primary=primary,
            confidence=confidence,
            all_signals=signals,
            scores=scores,
        )
