export type Bound = {
  min: number;
  max: number;
};

export function equalBounds(a: Bound, b: Bound) {
  return a.min === b.min && a.max === b.max;
}