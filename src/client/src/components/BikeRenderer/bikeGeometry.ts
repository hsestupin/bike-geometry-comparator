const WHEEL_RADIUS = 344;

export type Geometry = {
  stack: number;
  reach: number;
  headTubeAngle: number;
  seatTubeAngle: number;
  bbDrop: number;
  chainStay: number;
  headTubeLength: number;
  seatTubeLength: number;
  forkLength: number;
  forkRake: number;
  stemLength: number;
  stemAngle: number;
  spacers: number;
  seatPostLength: number;
  wheelRadius: number;
}

export const DEFAULT_GEOMETRY = {
  stack: 575,
  reach: 374,
  headTubeAngle: 71.3,
  seatTubeAngle: 73.7,
  bbDrop: 80,
  chainStay: 420,
  headTubeLength: 160,
  seatTubeLength: 500,
  forkLength: 371,
  forkRake: 53,
  stemLength: 100,
  stemAngle: -7,
  spacers: 20,
  seatPostLength: 180,
  wheelRadius: WHEEL_RADIUS
}
