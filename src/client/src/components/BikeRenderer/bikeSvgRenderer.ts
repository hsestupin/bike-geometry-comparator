import { Point } from "@/components/BikeRenderer/point";
import { Geometry } from "@/components/BikeRenderer/bikeGeometry";
import { calculateGeometry, D2R } from "@/components/BikeRenderer/bikeGeometryCalculator";

const CAMERA = {x: -850, y: -1050, w: 1900, h: 1400};

export type BikeShapeCssClasses = {
  component: string,
  dimLine: string
  joint: string,
  tire: string,
  rim: string,
  frameFill: string,
  forkFill: string,
  bar: string,
  text: string
}

export function renderBikeShapeSvg(geometry: Geometry, cssClasses: BikeShapeCssClasses): string {
  const d = calculateGeometry(geometry);
  const p = d.points;
  const v = d.vals;

  const framePath = `
      M ${p.basePoint.x},${-(p.basePoint.y)}
      L ${p.seatTubeTopPont.x},${-(p.seatTubeTopPont.y)}
      L ${p.headTubeTopPoint.x},${-(p.headTubeTopPoint.y)}
      L ${p.headTubeBottomPoint.x},${-(p.headTubeBottomPoint.y)}
      L ${p.headTubeJoin.x},${-(p.headTubeJoin.y)}
      L ${p.basePoint.x},${-(p.basePoint.y)}
      L ${p.rearHub.x},${-(p.rearHub.y)}
      L ${p.seatTubeTopPont.x},${-(p.seatTubeTopPont.y)}
    `;

  const forkPath = `
      M ${p.headTubeBottomPoint.x},${-(p.headTubeBottomPoint.y)}
      L ${p.forkHub.x},${-(p.forkHub.y)}
    `;

  const svg = `
            <svg viewBox="${CAMERA.x} ${CAMERA.y} ${CAMERA.w} ${CAMERA.h}"
                 onmousedown="startD(evt)" onmousemove="moveD(evt)" onmouseup="endD(evt)"
                 onmouseleave="endD(evt)" onwheel="zoom(evt)">
                <defs>
                    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
                        <path d="M0,0 L0,6 L9,3 z" fill="#555" />
                    </marker>
                    <marker id="arrowRev" markerWidth="10" markerHeight="10" refX="1" refY="3" orient="auto" markerUnits="strokeWidth">
                        <path d="M9,0 L9,6 L0,3 z" fill="#555" />
                    </marker>
                </defs>

                <line x1="-3000" y1="${-(v.groundY)}" x2="3000" y2="${-(v.groundY)}" class="${cssClasses.dimLine}" opacity="0.3"/>

                ${drawWheel(p.rearHub, geometry.wheelRadius, cssClasses)}
                ${drawWheel(p.forkHub, geometry.wheelRadius, cssClasses)}

                <line x1="${p.seatTubeTopPont.x}" y1="${-(p.seatTubeTopPont.y)}" x2="${p.saddlePoint.x}" y2="${-(p.saddlePoint.y)}" class="${cssClasses.component}"/>
                <path d="M${p.saddlePoint.x - 40},${-(p.saddlePoint.y)} L${p.saddlePoint.x + 80},${-(p.saddlePoint.y)}" class="${cssClasses.component}" stroke-width="12"/>

                <line x1="${p.headTubeTopPoint.x}" y1="${-(p.headTubeTopPoint.y)}" x2="${p.steerTop.x}" y2="${-(p.steerTop.y)}" class="${cssClasses.component}"/>
                <line x1="${p.steerTop.x}" y1="${-(p.steerTop.y)}" x2="${p.stemEnd.x}" y2="${-(p.stemEnd.y)}" class="${cssClasses.component}"/>
                <path d="M${p.stemEnd.x},${-(p.stemEnd.y)} l70,0 l0,70 l-40,0" class="${cssClasses.bar}"/>

                <path d="${framePath}" class="${cssClasses.frameFill}" />
                <path d="${forkPath}" class="${cssClasses.forkFill}" />

                <circle cx="${p.basePoint.x}" cy="${-(p.basePoint.y)}" r="10" class="${cssClasses.joint}" />

                <g>
                    <line x1="${p.basePoint.x}" y1="${-(p.headTubeTopPoint.y)}" x2="${p.headTubeTopPoint.x}" y2="${-(p.headTubeTopPoint.y)}" class="${cssClasses.dimLine}" stroke-dasharray="4,4" opacity="0.6"/>
                    ${arrow(p.basePoint.x, p.basePoint.y, p.basePoint.x, p.headTubeTopPoint.y, 'stack', 0, 20, 'vert', false, cssClasses)}
                    ${arrow(p.basePoint.x, p.headTubeTopPoint.y, p.headTubeTopPoint.x, p.headTubeTopPoint.y, 'reach', 100, 20, 'horiz', false, cssClasses)}
                    ${arrow(p.basePoint.x, p.basePoint.y, p.basePoint.x, p.rearHub.y, 'BB drop', -210, 20, 'vert', true, cssClasses)}
                    ${arrow(p.effectiveTopTubeLeftPoint.x, p.headTubeTopPoint.y, p.headTubeTopPoint.x, p.headTubeTopPoint.y, 'toptube length', 140, 20, 'horiz', true, cssClasses)}
                    ${arrow(p.basePoint.x, p.basePoint.y, p.seatTubeTopPont.x, p.seatTubeTopPont.y, 'seattube length', -60, 20, 'aligned', false, cssClasses)}
                    ${arrow(p.headTubeBottomPoint.x, p.headTubeBottomPoint.y, p.headTubeTopPoint.x, p.headTubeTopPoint.y, 'head tube length', 60, 20, 'aligned', false, cssClasses)}
                    ${arrow(p.rearHub.x, p.rearHub.y, p.forkHub.x, p.rearHub.y, 'wheelbase', -150, 20, 'horiz', false, cssClasses)}
                    ${arrow(p.rearHub.x, p.rearHub.y, p.basePoint.x, p.rearHub.y, 'rear center', -100, 20, 'horiz', false, cssClasses)}
                    ${arrow(p.basePoint.x, p.rearHub.y, p.forkHub.x, p.rearHub.y, 'front center', -100, 20, 'horiz', false, cssClasses)}
                    ${angleArc(p.basePoint.x, p.basePoint.y, 100, Math.PI, Math.PI - (geometry.seatTubeAngle * D2R), 'seat tube angle', cssClasses)}
                    ${angleArc(p.forkHub.x, p.rearHub.y, 120, Math.PI, Math.PI - (geometry.headTubeAngle * D2R), 'head tube angle', cssClasses)}
                </g>
            </svg>
        `;
  return svg;
}

function arrow(x1: number, y1: number, x2: number, y2: number, label: string, offset: number, txtOff = 20, type = "aligned", dashedExt = false, cssClasses: BikeShapeCssClasses) {
  const sx1 = x1, sy1 = -y1;
  const sx2 = x2, sy2 = -y2;

  let px1, py1, px2, py2;
  let ext1 = "", ext2 = "";

  const extStyle = dashedExt ? 'stroke-dasharray="4,4" opacity="0.6"' : 'opacity="0.5"';

  if (type === "horiz") {
    const yLevel = -(y1 + offset);
    px1 = sx1;
    py1 = yLevel;
    px2 = sx2;
    py2 = yLevel;
    ext1 = `<line x1="${sx1}" y1="${sy1}" x2="${sx1}" y2="${yLevel}" class="${cssClasses.dimLine}" ${extStyle}/>`;
    ext2 = `<line x1="${sx2}" y1="${sy2}" x2="${sx2}" y2="${yLevel}" class="${cssClasses.dimLine}" ${extStyle}/>`;
  } else if (type === "vert") {
    const xLevel = sx1 + offset;
    px1 = xLevel;
    py1 = sy1;
    px2 = xLevel;
    py2 = sy2;
    ext1 = `<line x1="${sx1}" y1="${sy1}" x2="${xLevel}" y2="${sy1}" class="${cssClasses.dimLine}" ${extStyle}/>`;
    ext2 = `<line x1="${sx2}" y1="${sy2}" x2="${xLevel}" y2="${sy2}" class="${cssClasses.dimLine}" ${extStyle}/>`;
  } else {
    const dx = sx2 - sx1, dy = sy2 - sy1;
    const len = Math.sqrt(dx * dx + dy * dy);
    if (len < 1) return '';
    const nx = -dy / len, ny = dx / len;
    px1 = sx1 + offset * nx;
    py1 = sy1 + offset * ny;
    px2 = sx2 + offset * nx;
    py2 = sy2 + offset * ny;
    ext1 = `<line x1="${sx1}" y1="${sy1}" x2="${px1}" y2="${py1}" class="${cssClasses.dimLine} ${extStyle}/>`;
    ext2 = `<line x1="${sx2}" y1="${sy2}" x2="${px2}" y2="${py2}" class="${cssClasses.dimLine}" ${extStyle}/>`;
  }

  const mx = (px1 + px2) / 2;
  const my = (py1 + py2) / 2;

  return `
        ${ext1}${ext2}
        <line x1="${px1}" y1="${py1}" x2="${px2}" y2="${py2}" class="${cssClasses.dimLine}" marker-start="url(#arrowRev)" marker-end="url(#arrow)"/>
        <text x="${mx}" y="${my - 5}" class="${cssClasses.text}" text-anchor="middle">${label}</text>
    `;
}

function angleArc(x: number, y: number, radius: number, startAngle: number, endAngle: number, label: string, cssClasses: BikeShapeCssClasses) {
  const sx = x + radius * Math.cos(startAngle);
  const sy = -(y + radius * Math.sin(startAngle));
  const ex = x + radius * Math.cos(endAngle);
  const ey = -(y + radius * Math.sin(endAngle));
  const largeArc = (endAngle - startAngle > Math.PI) ? 1 : 0;

  const midAngle = (startAngle + endAngle) / 2;
  const lx = x + (radius + 40) * Math.cos(midAngle);
  const ly = -(y + (radius + 40) * Math.sin(midAngle));

  const bl = `<line x1="${x - radius}" y1="${-y}" x2="${x + radius}" y2="${-y}" class="${cssClasses.dimLine}" opacity="0.3" stroke-dasharray="4,4"/>`;

  return `
        ${bl}
        <path d="M${sx},${sy} A${radius},${radius} 0 ${largeArc},1 ${ex},${ey}" class="${cssClasses.dimLine}" fill="none" marker-end="url(#arrow)"/>
        <text x="${lx}" y="${ly}" class="${cssClasses.text}" text-anchor="middle" dominant-baseline="middle">${label}</text>
    `;
}

function drawWheel(center: Point, radius: number, cssClasses: BikeShapeCssClasses) {
  const cy = -center.y;
  return `
        <circle cx="${center.x}" cy="${cy}" r="${radius}" class="${cssClasses.tire}"/>
        <circle cx="${center.x}" cy="${cy}" r="${radius - 15}" class="${cssClasses.rim}"/>
        <circle cx="${center.x}" cy="${cy}" r="6" fill="#fff" stroke="#333" stroke-width="2"/>
    `;
}