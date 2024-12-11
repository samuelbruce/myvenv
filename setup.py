
import argparse
import platform
import subprocess
import venv
from pathlib import Path

class MyVenv:
    this_path = Path(__file__).parent
    parent_path = this_path.parent
    paths = [parent_path]
    pip = None
    repo = None
    requirements = []
    scripts = []
    wheels = []
    venv_path = None
    
    def create_paths(self):
        with open(self.venv_path, "w") as f:
            for path in self.paths[1:]:
                print("Adding", str(path), "to PYTHONPATH")
                f.write(str(path)+"\n")
    
    def create_prefix(self, repo):
        for file in self.script_files:
            with open(file, "r") as f:
                lines = f.read()
                lines = lines.replace("(myvenv)", "({}-myvenv)".format(this.repo))
            with open(file, "w") as f:
                f.write(lines)
    
    def create_requirements(self):
        for requirements_txt in self.requirements:
            print("Installing", requirements_txt)
            subprocess.call([self.pip, "install", "-r", requirements_txt])
    
    def create_wheels(self):
        for wheel in self.wheels:
            print("Installing {}".format(wheel))
            subprocess.call([self.pip, "install", wheel])
    
    def delete(self):
        deleted = False
        for path in ["bin", "include", "Include", "lib", "lib64", "Lib", "Scripts", "pyvenv.cfg"]:
            path = self.this_path / path
            if path.exists():
                if path.is_dir():
                    for root, paths, files in path.walk(top_down=False):
                        for name in files:
                            (root / name).unlink()
                        for name in paths:
                            (root / name).rmdir()
                    path.rmdir()
                else:
                    path.unlink()
                deleted = True
            elif path.is_symlink():
                path.unlink()
                deleted = True
        if deleted:
            print("Deleted existing virtual environment")
    
    def find_packages(self):
        packages_path = self.parent_path / "packages"
        if packages_path.exists():
            print("Found", str(packages_path))
            self.paths += [packages_path]
            self.paths += [x for x in packages_path.iterdir() if x.is_dir()]
    
    def find_pip(self):
        if self.requirements or self.wheels:
            if "Linux" in platform.platform():
                self.pip = self.this_path / "bin" / "pip"
            elif "Windows" in platform.platform():
                self.pip = self.this_path / "Scripts" / "pip.exe"
    
    def find_repo(self):
        return
        # todo: attempt to get a name for the parent repo using "git remote show origin"
    
    def find_requirements(self):
        for path in self.paths:
            requirements = path / "requirements.txt"
            if requirements.exists():
                print("Found", str(requirements))
                self.requirements.append(requirements)
    
    def find_script_files(self):
        if "Linux" in platform.platform():
            self.script_files = [self.this_path / "bin" / x for x in ["activate", "activate.csh", "activate.fish"]]
        elif "Windows" in platform.platform():
            self.script_files = [self.this_path / "Scripts" / x for x in ["activate", "activate.bat"]]
    
    def find_wheels(self):
        for path in self.paths:
            for x in path.iterdir():
                if x.is_file() and x.suffix == ".whl":
                    print("Found", str(x))
                    self.wheels.append(x)
    
    def find_venv(self):
        if "Linux" in platform.platform():
            version = "python" + platform.version()[:platform.version().find(".",2)]
            packages_path = self.this_path / "lib" / version / "site-packages"
        elif "Windows" in platform.platform():
            packages_path = self.this_path / "Lib" / "site-packages"
        self.venv_path = packages_path / ".pth"
    
    def main(self):
        self.delete()
        print("Setting up new virtual environment")
        venv.create(self.this_path, with_pip=True)
        self.find_repo()
        if self.repo is not None:
            this.find_script_files()
            this.create_prefix()
        self.find_packages()
        self.find_venv()
        self.create_paths()
        self.find_requirements()
        self.find_wheels()
        self.create_requirements()
        self.create_wheels()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", action="store_true", help="Delete")
    args = vars(parser.parse_args())
    if args["d"]:
        MyVenv().delete()
    else:
        MyVenv().main()