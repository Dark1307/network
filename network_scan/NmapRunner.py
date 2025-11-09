"""
NmapRunner.py — Runs nmap commands for discovery and scanning (robust Windows support)
"""
import subprocess
import os
import datetime
import shutil

class NmapRunner:
    def __init__(self, nmap_explicit_path: str | None = None):
        """
        If `nmap_explicit_path` is provided, that path is used (useful when nmap isn't on PATH).
        Otherwise the runner tries shutil.which('nmap') and then a common Windows path.
        """
        self.output_dir = "reports"
        os.makedirs(self.output_dir, exist_ok=True)

        # Determine nmap path
        if nmap_explicit_path:
            self.nmap_path = nmap_explicit_path
        else:
            self.nmap_path = shutil.which("nmap") or r"C:\Program Files (x86)\Nmap\nmap.exe"

        # Normalize and verify
        self.nmap_path = os.path.normpath(self.nmap_path)
        if not os.path.isfile(self.nmap_path):
            # Do not crash here — raise a descriptive error
            raise RuntimeError(
                f"Nmap executable not found. Tried: {self.nmap_path}. "
                "Ensure nmap is installed and added to PATH, or pass explicit path to NmapRunner."
            )

    def _run_nmap(self, args, output_prefix):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.output_dir, f"{output_prefix}_{timestamp}.xml")

        # Build command. Using list form is safe with spaces in paths.
        cmd = [self.nmap_path, "-oX", filename] + list(args)
        print(f"[+] Running command: {' '.join(cmd)}")

        try:
            # capture stdout/stderr so we can log or include in exceptions if needed
            proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(proc.stdout)
            if proc.stderr:
                print("[nmap stderr]", proc.stderr)
        except FileNotFoundError as e:
            # This should not happen because we already checked, but handle it gracefully
            raise RuntimeError(f"Failed to execute nmap: executable not found at {self.nmap_path}") from e
        except subprocess.CalledProcessError as e:
            # Nmap returned non-zero; include stderr to help debugging
            stderr = e.stderr or ""
            stdout = e.stdout or ""
            raise RuntimeError(
                f"nmap failed with return code {e.returncode}\nstdout:\n{stdout}\nstderr:\n{stderr}"
            ) from e

        print(f"[+] Scan completed, output saved to {filename}")
        return filename

    def discovery(self, targets):
        """Run a simple ping/discovery scan"""
        return self._run_nmap(["-sn", targets], "discovery")

    def port_service_scan(self, targets, nse_safe=False):
        """Run a detailed port and service scan"""
        args = ["-sS", "-sV", "-T4", targets]
        if nse_safe:
            args += ["--script", "safe"]
        return self._run_nmap(args, "fullscan")
