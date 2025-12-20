import { Point } from "@/components/BikeRenderer/point";
import { Geometry } from "@/components/BikeRenderer/bikeGeometry";

export const D2R = Math.PI / 180;

export function calculateGeometry(
  geometry: Geometry,
) {
  let basePoint = {x: 0, y: 0};
  let headTubeTopPoint = {x: geometry.reach, y: geometry.stack};

  const headTubeRad = -geometry.headTubeAngle * D2R;
  let headTubeBottomPoint = {
    x: headTubeTopPoint.x + geometry.headTubeLength * Math.cos(headTubeRad),
    y: headTubeTopPoint.y + geometry.headTubeLength * Math.sin(headTubeRad)
  };

  // Calculate frame join point to clear tire
  let headTubeJoin = {
    x: headTubeBottomPoint.x + (headTubeTopPoint.x - headTubeBottomPoint.x) * 0.15,
    y: headTubeBottomPoint.y + (headTubeTopPoint.y - headTubeBottomPoint.y) * 0.15
  };

  const rakeRad = (-geometry.headTubeAngle + 90) * D2R;
  let forkHub = {
    x: headTubeBottomPoint.x + geometry.forkLenght * Math.cos(headTubeRad) + geometry.forkRake * Math.cos(rakeRad),
    y: headTubeBottomPoint.y + geometry.forkLenght * Math.sin(headTubeRad) + geometry.forkRake * Math.sin(rakeRad)
  };

  let rearHub = {
    x: -Math.sqrt(Math.max(0, geometry.chainStay * geometry.chainStay - geometry.bbDrop * geometry.bbDrop)),
    y: geometry.bbDrop
  };

  const seatTubeRad = (180 - geometry.seatTubeAngle) * D2R;
  let seatTubeTopPont = {
    x: basePoint.x + geometry.seatTubeLength * Math.cos(seatTubeRad),
    y: basePoint.y + geometry.seatTubeLength * Math.sin(seatTubeRad)
  };

  const t_ett = headTubeTopPoint.y / Math.sin(seatTubeRad);
  let effectiveTopTubeLeftPoint = {
    x: basePoint.x + t_ett * Math.cos(seatTubeRad),
    y: headTubeTopPoint.y
  };

  let saddlePoint = {
    x: seatTubeTopPont.x + geometry.seatPostLength * Math.cos(seatTubeRad),
    y: seatTubeTopPont.y + geometry.seatPostLength * Math.sin(seatTubeRad)
  };

  const upSteerRad = (-geometry.headTubeAngle + 180) * D2R;
  let steerTop = {
    x: headTubeTopPoint.x + geometry.spacers * Math.cos(upSteerRad),
    y: headTubeTopPoint.y + geometry.spacers * Math.sin(upSteerRad)
  };
  const stemAbsRad = (90 - geometry.headTubeAngle + geometry.stemAngle) * D2R;
  let stemEnd = {
    x: steerTop.x + geometry.stemLength * Math.cos(stemAbsRad),
    y: steerTop.y + geometry.stemLength * Math.sin(stemAbsRad)
  };

  const currentSlope = Math.atan2(forkHub.y - rearHub.y, forkHub.x - rearHub.x);
  const tilt = -currentSlope;
  const pivot = basePoint;

  headTubeTopPoint = rotate(headTubeTopPoint, pivot, tilt);
  headTubeBottomPoint = rotate(headTubeBottomPoint, pivot, tilt);
  headTubeJoin = rotate(headTubeJoin, pivot, tilt);
  forkHub = rotate(forkHub, pivot, tilt);
  rearHub = rotate(rearHub, pivot, tilt);
  seatTubeTopPont = rotate(seatTubeTopPont, pivot, tilt);
  effectiveTopTubeLeftPoint = rotate(effectiveTopTubeLeftPoint, pivot, tilt);
  saddlePoint = rotate(saddlePoint, pivot, tilt);
  steerTop = rotate(steerTop, pivot, tilt);
  stemEnd = rotate(stemEnd, pivot, tilt);

  const groundY = rearHub.y - geometry.wheelRadius;
  const wheelBase = Math.hypot(forkHub.x - rearHub.x, forkHub.y - rearHub.y);
  const trail = (geometry.wheelRadius * Math.cos(geometry.headTubeAngle * D2R) - geometry.forkRake) / Math.sin(geometry.headTubeAngle * D2R);
  const frontCenterLength = Math.hypot(forkHub.x - basePoint.x, forkHub.y - basePoint.y);
  const effectiveTopTubeLength = Math.hypot(headTubeTopPoint.x - effectiveTopTubeLeftPoint.x, headTubeTopPoint.y - effectiveTopTubeLeftPoint.y);
  const midTTY = (headTubeTopPoint.y + seatTubeTopPont.y) / 2;
  const standover = midTTY - groundY;

  return {
    points: {
      basePoint: basePoint,
      headTubeTopPoint: headTubeTopPoint,
      headTubeBottomPoint: headTubeBottomPoint,
      headTubeJoin: headTubeJoin,
      forkHub: forkHub,
      rearHub: rearHub,
      seatTubeTopPont: seatTubeTopPont,
      effectiveTopTubeLeftPoint: effectiveTopTubeLeftPoint,
      saddlePoint: saddlePoint,
      steerTop: steerTop,
      stemEnd: stemEnd
    },
    vals: {
      wheelBase: wheelBase,
      trail: trail,
      frontCenterLength: frontCenterLength,
      effTopTube: effectiveTopTubeLength,
      standover: standover,
      groundY: groundY,
    }
  };
}

function rotate(point: Point, pivotPoint: Point, angle: number): Point {
  const dx = point.x - pivotPoint.x;
  const dy = point.y - pivotPoint.y;
  return {
    x: pivotPoint.x + dx * Math.cos(angle) - dy * Math.sin(angle),
    y: pivotPoint.y + dx * Math.sin(angle) + dy * Math.cos(angle)
  };
}