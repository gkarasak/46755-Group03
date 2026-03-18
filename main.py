import subprocess
import sys
import os

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
HOUR        = 18
STEPS_DIR   = 'Steps'
RESULTS_DIR = 'Results'
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# ──────────────────────────────────────────────────────────────────────────────

def run_notebook(notebook_path, hour):
    print(f"\n{'='*60}")
    print(f"Running: {notebook_path}")
    print(f"{'='*60}")

    env                = os.environ.copy()
    env['HOUR']        = str(hour)
    env['PYTHONPATH']  = PROJECT_ROOT

    result = subprocess.run(
        [
            sys.executable, '-m', 'nbconvert',
            '--to', 'notebook',
            '--execute',
            '--inplace',
            '--ExecutePreprocessor.timeout=600',
            notebook_path
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=PROJECT_ROOT
    )

    if result.returncode == 0:
        print(f"  ✓ {notebook_path} completed successfully")
    else:
        print(f"  ✗ {notebook_path} FAILED")
        print(f"  Error: {result.stderr[-2000:]}")
        sys.exit(1)


def run_py(script_path, hour):
    print(f"\n{'='*60}")
    print(f"Running: {script_path}")
    print(f"{'='*60}")

    env               = os.environ.copy()
    env['HOUR']       = str(hour)
    env['PYTHONPATH'] = PROJECT_ROOT

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True,
        text=True,
        env=env,
        cwd=PROJECT_ROOT
    )

    if result.returncode == 0:
        print(f"  ✓ {script_path} completed successfully")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"  ✗ {script_path} FAILED")
        print(f"  Error: {result.stderr[-500:]}")
        sys.exit(1)


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":

    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"\n{'#'*60}")
    print(f"  RUNNING ALL STEPS FOR HOUR {HOUR}")
    print(f"{'#'*60}")

    # Step 1 — DA Copperplate market
    run_notebook(os.path.join(STEPS_DIR, 'Assignment_1_step_1.ipynb'), HOUR)

    # Step 2 — Storage
    run_py(os.path.join(STEPS_DIR, 'Assignment_1_step_2.py'), HOUR)

    # Step 3 — Nodal market
    run_notebook(os.path.join(STEPS_DIR, 'Assignment_1_step_3_nodal.ipynb'), HOUR)

    # Step 3 — Zonal market
    run_notebook(os.path.join(STEPS_DIR, 'Assignment_1_step_3_zonal.ipynb'), HOUR)

    # Step 5 — Balancing market
    run_notebook(os.path.join(STEPS_DIR, 'Assignment_1_step_5.ipynb'), HOUR)

    # Step 6 — Reserve + DA sequential (European) and joint (US)
    run_notebook(os.path.join(STEPS_DIR, 'Assignment_1_step_6.ipynb'), HOUR)

    print(f"\n{'#'*60}")
    print(f"  ALL STEPS DONE — GO CHECK THE OUTPUTS")
    print(f"  Plots saved in:  ./{RESULTS_DIR}/")
    print(f"  JSON results:    {RESULTS_DIR}/DA_results_step1.json")
    print(f"{'#'*60}\n")