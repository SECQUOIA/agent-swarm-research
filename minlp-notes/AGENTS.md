# Verification during local work

Run targeted checks for the topic or modules being changed. Do not run
project-wide verification locally, and do not inspect CI status or logs to
duplicate those checks. CI handles project-wide verification. Record the
targeted commands actually run and distinguish their results from CI checks.

Work only on the topic the user has authorized. Completing one topic does not
authorize starting another when the user has requested a stop.
