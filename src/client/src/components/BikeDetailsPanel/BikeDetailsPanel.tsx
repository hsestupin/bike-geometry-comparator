import { Bike } from '@/types/Bike';
import Panel from '@/components/Panel/Panel';
import styles from './BikeDetailsPanel.module.css';

type Props = { bike: Bike; onClose: () => void };

export default function BikeDetailsPanel({ bike, onClose }: Props) {
  return (
    <Panel className={styles.panel} aria-label="Bike details">
      <div className={styles.header}>
        <h3 className={styles.title}>{bike.brand} {bike.model}</h3>
        <button className={styles.close} onClick={onClose} aria-label="Close">✕</button>
      </div>
      <div className={styles.body}>
        <dl className={styles.dl}>
          <div className={styles.row}><dt>Year</dt><dd>{bike.year}</dd></div>
          <div className={styles.row}><dt>Size</dt><dd>{bike.size}</dd></div>
          <div className={styles.row}><dt>Stack</dt><dd>{bike.stack} mm</dd></div>
          <div className={styles.row}><dt>Reach</dt><dd>{bike.reach} mm</dd></div>
        </dl>
      </div>
    </Panel>
  );
}
