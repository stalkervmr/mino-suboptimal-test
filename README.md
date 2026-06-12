# Suboptimal Test Solver

A deliberately-suboptimal IntentSolver used by the subnet112 team to validate
the submission scoring pipeline and the per-case feedback report on the live
leader validator. It subclasses the baseline swap solver but solves only every
other intent, so it produces valid plans on a subset while scoring well below
the champion. Not intended to win any round.
