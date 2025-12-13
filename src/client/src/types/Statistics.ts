import { Bound } from "@/types/Bound";

export type Statistics = {
  stack: Bound,
  reach: Bound,
}

export const EMPTY_STATISTICS: Statistics = {
  stack: { min: 0, max: 0 },
  reach: { min: 0, max: 0 },
}