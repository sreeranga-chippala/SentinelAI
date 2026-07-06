"""
scheduler.py

SentinelAI Scheduler

Responsibilities
----------------
1. Execute Coordinator every N seconds.
2. Handle start/stop.
3. Continue even if one cycle fails.
4. Measure execution time.
5. Support changing disaster location.
"""

from __future__ import annotations

import threading
import time
import traceback


class Scheduler:

    def __init__(
        self,
        coordinator,
        disaster_area: str = "Bengaluru",
        interval: int = 30,
    ):

        self.coordinator = coordinator

        self.disaster_area = disaster_area

        self.interval = interval

        self.running = False

        self.thread = None

    # ---------------------------------------------------------

    def _run(self):

        while self.running:

            start = time.perf_counter()

            try:

                self.coordinator.run(
                    self.disaster_area
                )

            except Exception:

                traceback.print_exc()

            elapsed = (
                time.perf_counter() - start
            )

            sleep_time = max(
                0,
                self.interval - elapsed,
            )

            time.sleep(sleep_time)

    # ---------------------------------------------------------

    def start(self):

        if self.running:

            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

        self.thread.start()

        print(
            f"Scheduler started "
            f"({self.interval}s interval)"
        )

    # ---------------------------------------------------------

    def stop(self):

        self.running = False

        if self.thread is not None:

            self.thread.join(timeout=5)

        print("Scheduler stopped.")

    # ---------------------------------------------------------

    def is_running(self):

        return self.running

    # ---------------------------------------------------------

    def run_once(self):

        self.coordinator.run(
            self.disaster_area
        )

    # ---------------------------------------------------------

    def set_interval(
        self,
        seconds: int,
    ):

        self.interval = seconds

    # ---------------------------------------------------------

    def set_disaster_area(
        self,
        area: str,
    ):

        self.disaster_area = area