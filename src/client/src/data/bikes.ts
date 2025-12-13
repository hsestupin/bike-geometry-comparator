import { Bike } from '@/types/Bike';

export const bikes: Bike[] = [
  { brand: 'Trek', model: 'Slash 8', year: 2024, size: 'M', stack: 630, reach: 470 },
  { brand: 'Trek', model: 'Fuel EX 9.8', year: 2023, size: 'L', stack: 640, reach: 485 },
  { brand: 'Specialized', model: 'Stumpjumper Comp', year: 2022, size: 'M', stack: 620, reach: 455 },
  { brand: 'Specialized', model: 'Enduro Elite', year: 2024, size: 'L', stack: 650, reach: 495 },
  { brand: 'Giant', model: 'Trance X 1', year: 2023, size: 'M', stack: 615, reach: 460 },
  { brand: 'Giant', model: 'Reign Advanced', year: 2024, size: 'L', stack: 645, reach: 500 },
  { brand: 'Canyon', model: 'Spectral 29 CF', year: 2022, size: 'M', stack: 610, reach: 460 },
  { brand: 'Canyon', model: 'Strive CFR', year: 2024, size: 'L', stack: 648, reach: 505 },
  { brand: 'Santa Cruz', model: 'Hightower', year: 2023, size: 'M', stack: 625, reach: 470 },
  { brand: 'Santa Cruz', model: 'Megatower', year: 2024, size: 'L', stack: 655, reach: 500 },
  { brand: 'Yeti', model: 'SB130', year: 2021, size: 'M', stack: 615, reach: 460 },
  { brand: 'Yeti', model: 'SB160', year: 2024, size: 'L', stack: 652, reach: 505 },
  { brand: 'Orbea', model: 'Occam M10', year: 2023, size: 'M', stack: 618, reach: 465 },
  { brand: 'Orbea', model: 'Rallon M-Team', year: 2024, size: 'L', stack: 646, reach: 500 }
];

export const stackBounds = {
  min: Math.min(...bikes.map(b => b.stack)),
  max: Math.max(...bikes.map(b => b.stack)),
};

export const reachBounds = {
  min: Math.min(...bikes.map(b => b.reach)),
  max: Math.max(...bikes.map(b => b.reach)),
};

export const brands = Array.from(new Set(bikes.map(b => b.brand))).sort();
