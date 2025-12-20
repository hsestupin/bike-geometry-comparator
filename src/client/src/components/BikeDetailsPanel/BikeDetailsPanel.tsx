import { useEffect, useId, useState } from 'react';
import Panel from '@/components/Panel/Panel';
import styles from './BikeDetailsPanel.module.css';
import { BikeDetailedInfo } from "@/types/BikeDetailedInfo";
import BikeShape from "@/components/BikeRenderer/BikeShape";
import { DEFAULT_GEOMETRY } from "@/components/BikeRenderer/bikeGeometry";

type BikeDetailsPanelProps = {
  bike: BikeDetailedInfo;
  onClose: () => void
};

type BikeDetailsRowProps = {
  label: string;
  value: number | string | undefined | null;
  unit?: string
};

const EXPANDED_STORAGE_KEY = 'bike-details-expanded';

const detailedRows = (bike: BikeDetailedInfo): BikeDetailsRowProps[] => {
  return [
    {label: 'Top tube length', value: bike.topTubeLength, unit: 'mm'},
    {label: 'Seat tube length', value: bike.seatTubeLength, unit: 'mm'},
    {label: 'Seat tube angle', value: bike.seatTubeAngle, unit: '°'},
    {label: 'Seatpost length', value: bike.seatPostLength, unit: 'mm'},
    {label: 'Head tube angle', value: bike.headTubeAngle, unit: '°'},
    {label: 'Chainstay', value: bike.chainStay, unit: 'mm'},
    {label: 'Fork rake', value: bike.forkRake, unit: 'mm'},
    {label: 'Wheelbase', value: bike.wheelbase, unit: 'mm'},
    {label: 'Trail', value: bike.trail, unit: 'mm'},
    {label: 'BB drop', value: bike.bbDrop, unit: 'mm'},
    {label: 'Front center', value: bike.frontCenterDistance, unit: 'mm'},
    {label: 'Head tube length', value: bike.headTubeLength, unit: 'mm'},
    {label: 'Stem length', value: bike.stemLength, unit: 'mm'},
    {label: 'Fork length (axle-to-crown)', value: bike.forkLength, unit: 'mm'},
    {label: 'Standover height', value: bike.standoverHeight, unit: 'mm'},
    {label: 'Wheel size', value: bike.wheelSize},
    {label: 'Rider height range', value: bike.bodyHeightRange},
    {label: 'Saddle height range', value: bike.seatHeightRange},
    {label: 'Seatpost diameter', value: bike.seatPostDiameter},
  ];
}

function BikeDetailRow(props: BikeDetailsRowProps) {
  const {label, value, unit} = props;
  return (
    <div className={styles.row}>
      <dt>{label}</dt>
      <dd className={styles.value}>{value}{unit && ` ${unit}`}</dd>
    </div>
  );
}

export default function BikeDetailsPanel({bike, onClose}: BikeDetailsPanelProps) {
  const [expanded, setExpanded] = useState<boolean>(false);
  const detailsId = useId();

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

  return (
    <Panel className={`${styles.panel} ${expanded ? styles.expanded : ''}`} aria-label="BikeShape details">
      <div className={styles.header}>
        <h3 className={styles.title}>{bike.brand} {bike.model}</h3>
        <button className={styles.close} onClick={onClose} aria-label="Close">✕</button>
      </div>
      <div className={styles.body}>
        <dl className={styles.dl}>
          <BikeDetailRow label={"Year"} value={bike.year}/>
          <BikeDetailRow label={"Size"} value={bike.size}/>
          <BikeDetailRow label={"Stack"} value={bike.stack} unit={"mm"}/>
          <BikeDetailRow label={"Reach"} value={bike.reach} unit={"mm"}/>
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
              {detailedRows(bike)
                .map((row, idx) => (
                  <BikeDetailRow {...row} key={`${row.label}-${idx}`}/>
                ))
              }
            </dl>
          </div>
        )}
      </div>
      <div className={styles.shape}>
        <BikeShape
          geometry={{
            stack: bike.stack ?? DEFAULT_GEOMETRY.stack,
            reach: bike.reach ?? DEFAULT_GEOMETRY.reach,
            headTubeAngle: bike.headTubeAngle ?? DEFAULT_GEOMETRY.headTubeAngle,
            seatTubeAngle: bike.seatTubeAngle ?? DEFAULT_GEOMETRY.seatTubeAngle,
            bbDrop: bike.bbDrop ?? DEFAULT_GEOMETRY.bbDrop,
            chainStay: bike.chainStay ?? DEFAULT_GEOMETRY.chainStay,
            headTubeLength: bike.headTubeLength ?? DEFAULT_GEOMETRY.headTubeLength,
            seatTubeLength: bike.seatTubeLength ?? DEFAULT_GEOMETRY.seatTubeLength,
            seatPostLength: bike.seatPostLength ?? DEFAULT_GEOMETRY.seatPostLength,
            forkLenght: bike.forkLength ?? DEFAULT_GEOMETRY.forkLenght,
            forkRake: bike.forkRake ?? DEFAULT_GEOMETRY.forkRake,
            stemLength: bike.stemLength ?? DEFAULT_GEOMETRY.stemLength,
            stemAngle: DEFAULT_GEOMETRY.stemAngle,
            spacers: DEFAULT_GEOMETRY.spacers,
            wheelRadius: DEFAULT_GEOMETRY.wheelRadius
          }}
        />
      </div>
    </Panel>
  );
}
