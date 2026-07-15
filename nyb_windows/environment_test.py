"""
environment_test.py

A quick, Windows-safe sanity check for the two things that most often break
during the QuickKart labs: multiprocessing and matplotlib.

Run it exactly as-is, before the actual lab:
    python environment_test.py

If both tests print "PASSED", your machine is ready for the notebooks.
If the multiprocessing test hangs on Windows, see the note at the bottom
of this file.
"""

import os
import sys
import time
from multiprocessing import Pool


# ----------------------------------------------------------------------
# Test 1: multiprocessing
# ----------------------------------------------------------------------
def square(n):
    """A trivial function run in parallel -- just needs to prove that
    worker processes can start, run, and return a result."""
    return n * n


def test_multiprocessing():
    print("\n[1/2] Testing multiprocessing.Pool ...")
    start = time.time()
    try:
        with Pool(3) as pool:
            results = pool.map(square, [1, 2, 3, 4, 5])
        elapsed = time.time() - start

        expected = [1, 4, 9, 16, 25]
        if results == expected:
            print(f"      PASSED  ({elapsed:.2f}s) -- got {results}")
            return True
        else:
            print(f"      FAILED  -- expected {expected}, got {results}")
            return False
    except Exception as e:
        print(f"      FAILED  -- {type(e).__name__}: {e}")
        return False


# ----------------------------------------------------------------------
# Test 2: matplotlib
# ----------------------------------------------------------------------
def test_matplotlib():
    print("[2/2] Testing matplotlib ...")
    try:
        import matplotlib
        matplotlib.use("Agg")  # no GUI needed -- just prove it can render and save
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(["North", "South", "West"], [3, 5, 2], color="#1F4E79")
        ax.set_title("Environment test chart")
        out_path = os.path.join(os.getcwd(), "environment_test_chart.png")
        fig.savefig(out_path)
        plt.close(fig)

        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            print(f"      PASSED  -- chart saved to {out_path}")
            return True
        else:
            print("      FAILED  -- chart file was not created")
            return False
    except Exception as e:
        print(f"      FAILED  -- {type(e).__name__}: {e}")
        return False


# ----------------------------------------------------------------------
# Run both tests
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("QuickKart lab environment check")
    print(f"Python {sys.version.split()[0]} on {sys.platform}")
    print("=" * 50)

    mp_ok = test_multiprocessing()
    plt_ok = test_matplotlib()

    print("\n" + "=" * 50)
    if mp_ok and plt_ok:
        print("ALL TESTS PASSED -- you're ready for the lab notebooks.")
    else:
        print("SOME TESTS FAILED -- see notes below before the lab.")
    print("=" * 50)

    if not mp_ok:
        print(
            "\nmultiprocessing note (Windows users):\n"
            "If this hung instead of failing cleanly, it's the classic Windows\n"
            "'spawn' issue: worker processes re-import this file to find the\n"
            "square() function. That's exactly why this script wraps its Pool\n"
            "call in `if __name__ == \"__main__\":` -- if you copy this pattern\n"
            "into a notebook and it STILL hangs, switch to\n"
            "concurrent.futures.ThreadPoolExecutor for that notebook instead."
        )
