// SM-2 inspired SRS scheduler with confidence rating.
// confidence: 1=guess (au hasard), 2=uncertain, 3=sure
// stability: days until next review (fractional allowed — 0.5 = 12 h)
// state: 0=new  1=learning  2=review  3=relearning

export type SRSInput = {
  reps: number;
  lapses: number;
  stability: number;
  difficulty_fsrs: number;
  state: number;
};

export type SRSOutput = {
  reps: number;
  lapses: number;
  stability: number;
  difficulty_fsrs: number;
  state: number;
  dueAt: Date;
};

// Interval multipliers by confidence (applied to current stability for review state)
const MULT: Record<1 | 2 | 3, number> = { 1: 1.3, 2: 1.8, 3: 2.5 };
// First-review interval (days) by confidence
const FIRST: Record<1 | 2 | 3, number> = { 1: 0.5, 2: 1, 3: 2 };
// Second-review interval (days) by confidence
const SECOND: Record<1 | 2 | 3, number> = { 1: 1, 2: 4, 3: 6 };

export function schedule(
  input: SRSInput,
  isCorrect: boolean,
  confidence: 1 | 2 | 3
): SRSOutput {
  const { reps, lapses, stability, difficulty_fsrs, state } = input;
  const newReps = reps + 1;

  if (!isCorrect) {
    return {
      reps: newReps,
      lapses: lapses + 1,
      stability: 0.5,
      difficulty_fsrs: parseFloat(Math.min(1, difficulty_fsrs + 0.1).toFixed(4)),
      state: state === 0 ? 1 : 3,
      dueAt: new Date(Date.now() + 10 * 60_000),
    };
  }

  let s: number;
  if (reps === 0) {
    s = FIRST[confidence];
  } else if (reps === 1 && state <= 1) {
    s = SECOND[confidence];
  } else if (state === 3) {
    // Recovering from lapse — conservative growth
    s = Math.max(1, stability * 0.5 * MULT[confidence]);
  } else {
    s = Math.max(stability * MULT[confidence], stability + 1);
  }
  s = parseFloat(Math.min(s, 60).toFixed(4));

  const newState = state === 3 ? 2 : newReps >= 3 || s >= 6 ? 2 : 1;
  const newDifficulty = parseFloat(
    Math.max(0, Math.min(1, difficulty_fsrs + (2 - confidence) * 0.05)).toFixed(4)
  );

  return {
    reps: newReps,
    lapses,
    stability: s,
    difficulty_fsrs: newDifficulty,
    state: newState,
    dueAt: new Date(Date.now() + s * 86_400_000),
  };
}
