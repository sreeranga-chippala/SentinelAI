"""
scheduler.py

Scheduler for SentinelAI.

Responsibilities
----------------
1. Execute Coordinator every N seconds.
2. Handle start/stop.
3. Continue execution even if one cycle fails.
"""

import threading
import time


class Scheduler:

    def __init__(
        self,
        coordinator,
        interval=30
    ):

        self.coordinator = coordinator

        self.interval = interval

        self.running = False

        self.thread = None

    # ---------------------------------------------------------

    def _run(self):

        while self.running:

            start = time.time()

            try:

                self.coordinator.execute_cycle()

            except Exception as e:

                print(f"[Scheduler] {e}")

            elapsed = time.time() - start

            sleep_time = max(

                0,

                self.interval - elapsed

            )

            time.sleep(sleep_time)

    # ---------------------------------------------------------

    def start(self):

        if self.running:

            return

        self.running = True

        self.thread = threading.Thread(

            target=self._run,

            daemon=True

        )

        self.thread.start()

        print(

            f"Scheduler started ({self.interval}s interval)."

        )

    # ---------------------------------------------------------

    def stop(self):

        self.running = False

        print("Scheduler stopped.")

    # ---------------------------------------------------------

    def is_running(self):

        return self.running

    # ---------------------------------------------------------

    def run_once(self):

        self.coordinator.execute_cycle()