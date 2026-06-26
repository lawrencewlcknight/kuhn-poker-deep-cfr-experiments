"""Reusable code for Kuhn poker Deep CFR experiments."""

from .constants import (
    DEFAULT_AVERAGE_POLICY_VALUE_TARGET,
    DEFAULT_EXPLOITABILITY_THRESHOLD,
    DEFAULT_SOLVER_BATCH_SIZE,
    KUHN_GAME_VALUE_PLAYER_0,
)


def __getattr__(name: str):
    if name in {"DeepCFRSolver", "SolveResult"}:
        from .solver import DeepCFRSolver, SolveResult

        return {"DeepCFRSolver": DeepCFRSolver, "SolveResult": SolveResult}[name]
    if name == "cleanup_training_memory":
        from .experiment_utils import cleanup_training_memory

        return cleanup_training_memory
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "DeepCFRSolver",
    "SolveResult",
    "DEFAULT_AVERAGE_POLICY_VALUE_TARGET",
    "KUHN_GAME_VALUE_PLAYER_0",
    "DEFAULT_EXPLOITABILITY_THRESHOLD",
    "DEFAULT_SOLVER_BATCH_SIZE",
    "cleanup_training_memory",
]
