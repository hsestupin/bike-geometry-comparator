import { useEffect, useId, useState } from 'react';
import Panel from '@/components/Panel/Panel';
import styles from './BikeDetailsPanel.module.css';
import { BikeDetailedInfo } from "@/types/BikeDetailedInfo";
import BikeShape from "@/components/BikeRenderer/BikeShape";
import { DEFAULT_GEOMETRY, Geometry } from "@/components/BikeRenderer/bikeGeometry";

type BikeDetailsPanelProps = {
  bike: BikeDetailedInfo;
  pinnedBike: BikeDetailedInfo | null;
  onPin: (bike: BikeDetailedInfo) => void;
  onClose: () => void
};

type BikeDetailsRowProps = {
  label: string;
  value: number | string | undefined | null;
  pinnedValue?: number | string | undefined | null;
  unit?: string;
  comparing: boolean;
};

const EXPANDED_STORAGE_KEY = 'bike-details-expanded';

function formatValue(value: number | string | undefined | null, unit?: string): string {
  if (value == null) return '-';
  return `${value}${unit ? ` ${unit}` : ''}`;
}

const detailedRows = (bike: BikeDetailedInfo, pinned: BikeDetailedInfo | null): Omit<BikeDetailsRowProps, 'comparing'>[] => {
  return [
    {label: 'Top tube length', value: bike.topTubeLength, pinnedValue: pinned?.topTubeLength, unit: 'mm'},
    {label: 'Seat tube length', value: bike.seatTubeLength, pinnedValue: pinned?.seatTubeLength, unit: 'mm'},
    {label: 'Seat tube angle', value: bike.seatTubeAngle, pinnedValue: pinned?.seatTubeAngle, unit: '°'},
    {label: 'Seatpost length', value: bike.seatPostLength, pinnedValue: pinned?.seatPostLength, unit: 'mm'},
    {label: 'Head tube angle', value: bike.headTubeAngle, pinnedValue: pinned?.headTubeAngle, unit: '°'},
    {label: 'Chainstay', value: bike.chainStay, pinnedValue: pinned?.chainStay, unit: 'mm'},
    {label: 'Fork rake', value: bike.forkRake, pinnedValue: pinned?.forkRake, unit: 'mm'},
    {label: 'Wheelbase', value: bike.wheelbase, pinnedValue: pinned?.wheelbase, unit: 'mm'},
    {label: 'Trail', value: bike.trail, pinnedValue: pinned?.trail, unit: 'mm'},
    {label: 'BB drop', value: bike.bbDrop, pinnedValue: pinned?.bbDrop, unit: 'mm'},
    {label: 'Front center', value: bike.frontCenterDistance, pinnedValue: pinned?.frontCenterDistance, unit: 'mm'},
    {label: 'Head tube length', value: bike.headTubeLength, pinnedValue: pinned?.headTubeLength, unit: 'mm'},
    {label: 'Stem length', value: bike.stemLength, pinnedValue: pinned?.stemLength, unit: 'mm'},
    {label: 'Fork length (axle-to-crown)', value: bike.forkLength, pinnedValue: pinned?.forkLength, unit: 'mm'},
    {label: 'Standover height', value: bike.standoverHeight, pinnedValue: pinned?.standoverHeight, unit: 'mm'},
    {label: 'Wheel size', value: bike.wheelSize, pinnedValue: pinned?.wheelSize},
    {label: 'Rider height range', value: bike.bodyHeightRange, pinnedValue: pinned?.bodyHeightRange},
    {label: 'Saddle height range', value: bike.seatHeightRange, pinnedValue: pinned?.seatHeightRange},
    {label: 'Seatpost diameter', value: bike.seatPostDiameter, pinnedValue: pinned?.seatPostDiameter},
  ];
}

function isSameBike(a: BikeDetailedInfo, b: BikeDetailedInfo): boolean {
  return a.brand === b.brand && a.model === b.model && a.year === b.year && a.size === b.size;
}

function BikeDetailRow(props: BikeDetailsRowProps) {
  const {label, value, pinnedValue, unit, comparing} = props;
  return (
    <div className={`${styles.row} ${comparing ? styles.rowComparing : ''}`}>
      <dt>{label}</dt>
      <dd className={styles.value}>{formatValue(value, unit)}</dd>
      {comparing && <dd className={styles.pinnedValue}>{formatValue(pinnedValue, unit)}</dd>}
    </div>
  );
}

function bikeToGeometry(bike: BikeDetailedInfo): Geometry {
  return {
    stack: bike.stack ?? DEFAULT_GEOMETRY.stack,
    reach: bike.reach ?? DEFAULT_GEOMETRY.reach,
    headTubeAngle: bike.headTubeAngle ?? DEFAULT_GEOMETRY.headTubeAngle,
    seatTubeAngle: bike.seatTubeAngle ?? DEFAULT_GEOMETRY.seatTubeAngle,
    bbDrop: bike.bbDrop ?? DEFAULT_GEOMETRY.bbDrop,
    chainStay: bike.chainStay ?? DEFAULT_GEOMETRY.chainStay,
    headTubeLength: bike.headTubeLength ?? DEFAULT_GEOMETRY.headTubeLength,
    seatTubeLength: bike.seatTubeLength ?? DEFAULT_GEOMETRY.seatTubeLength,
    seatPostLength: bike.seatPostLength ?? DEFAULT_GEOMETRY.seatPostLength,
    forkLength: bike.forkLength ?? DEFAULT_GEOMETRY.forkLength,
    forkRake: bike.forkRake ?? DEFAULT_GEOMETRY.forkRake,
    stemLength: bike.stemLength ?? DEFAULT_GEOMETRY.stemLength,
    stemAngle: DEFAULT_GEOMETRY.stemAngle,
    spacers: DEFAULT_GEOMETRY.spacers,
    wheelRadius: DEFAULT_GEOMETRY.wheelRadius,
  };
}

export default function BikeDetailsPanel({bike, pinnedBike, onPin, onClose}: BikeDetailsPanelProps) {
  const [expanded, setExpanded] = useState<boolean>(false);
  const detailsId = useId();

  const isPinned = pinnedBike !== null;
  const showComparison = pinnedBike !== null && !isSameBike(bike, pinnedBike);

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(EXPANDED_STORAGE_KEY);
      if (saved !== null) setExpanded(saved === 'true');
    } catch { /* ignore */
    }
  }, []);

  useEffect(() => {
    try {
      window.localStorage.setItem(EXPANDED_STORAGE_KEY, String(expanded));
    } catch { /* ignore */
    }
  }, [expanded]);

  const toggleExpanded = () => setExpanded(prev => !prev);

  const pinned = showComparison ? pinnedBike : null;

  return (
    <Panel className={`${styles.panel} ${expanded ? styles.expanded : ''}`} aria-label="BikeShape details">
      <div className={styles.header}>
        <h3 className={styles.title}>{bike.brand} {bike.model}</h3>
        <div className={styles.headerActions}>
          <button
            className={`${styles.pinBtn} ${isPinned ? styles.pinBtnActive : ''}`}
            onClick={() => onPin(bike)}
            aria-label={isPinned ? 'Unpin bike' : 'Pin bike for comparison'}
            title={isPinned ? 'Unpin' : 'Pin for comparison'}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 17v5"/>
              <path d="M5 17h14"/>
              <path d="M15 3.5L9.5 9 5 17l12 0-4.5-8L17 3.5a1.5 1.5 0 0 0-2 0z"/>
            </svg>
          </button>
          <button className={styles.close} onClick={onClose} aria-label="Close">✕</button>
        </div>
      </div>
      <div className={styles.body}>
        {showComparison && (
          <div className={styles.columnHeaders}>
            <span/>
            <span className={styles.columnLabel}>Selected</span>
            <span className={styles.columnLabel}>Pinned</span>
          </div>
        )}
        <dl className={styles.dl}>
          <BikeDetailRow label={"Year"} value={bike.year} pinnedValue={pinned?.year} comparing={showComparison}/>
          <BikeDetailRow label={"Size"} value={bike.size} pinnedValue={pinned?.size} comparing={showComparison}/>
          <BikeDetailRow label={"Stack"} value={bike.stack} pinnedValue={pinned?.stack} unit={"mm"} comparing={showComparison}/>
          <BikeDetailRow label={"Reach"} value={bike.reach} pinnedValue={pinned?.reach} unit={"mm"} comparing={showComparison}/>
        </dl>
        <div className={styles.moreWrapper}>
          <button
            className={styles.toggle}
            onClick={toggleExpanded}
            aria-expanded={expanded}
            aria-controls={detailsId}
          >
            {expanded ? 'Hide detailed geometry' : 'Show detailed geometry'}
          </button>
        </div>
        {expanded && (
          <div id={detailsId} className={styles.details}>
            <dl className={styles.dl}>
              {detailedRows(bike, pinned)
                .map((row, idx) => (
                  <BikeDetailRow {...row} comparing={showComparison} key={`${row.label}-${idx}`}/>
                ))
              }
            </dl>
          </div>
        )}
      </div>
      <div className={styles.shape}>
        <BikeShape
          geometry={bikeToGeometry(bike)}
          referenceGeometry={showComparison ? bikeToGeometry(pinnedBike) : undefined}
        />
      </div>
    </Panel>
  );
}
