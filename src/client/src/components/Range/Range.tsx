import styles from './Range.module.css';

type Props = {
  min: number;
  max: number;
  value: [number, number];
  step?: number;
  onChange: (value: [number, number]) => void;
  label: string;
  unit?: string;
};

export default function Range({ min, max, value, step = 1, onChange, label, unit = '' }: Props) {
  const [from, to] = value;
  const clamp = (v: number) => Math.min(max, Math.max(min, v));
  const pct = (v: number) => ((v - min) / (max - min)) * 100;

  const onFromChange = (v: number) => {
    const next = clamp(v);
    onChange([Math.min(next, to), to]);
  };
  const onToChange = (v: number) => {
    const next = clamp(v);
    onChange([from, Math.max(next, from)]);
  };

  return (
    <div className={styles.wrap}>
      <label className={styles.label}>{label}</label>
      <div className={styles.row}>
        <input
          className={styles.input}
          type="number"
          min={min}
          max={to}
          value={from}
          onChange={(e) => onFromChange(Number(e.target.value))}
        />
        <span className={styles.unit}>{unit}</span>
        <input
          className={styles.input}
          type="number"
          min={from}
          max={max}
          value={to}
          onChange={(e) => onToChange(Number(e.target.value))}
        />
        <span className={styles.unit}>{unit}</span>
      </div>
      <div className={styles.sliderWrap}>
        <div className={styles.track} />
        <div
          className={styles.range}
          style={{ left: `${pct(from)}%`, right: `${100 - pct(to)}%` }}
        />
        <input
          aria-label={`${label} from`}
          className={`${styles.thumb} ${styles.thumbLeft}`}
          type="range"
          min={min}
          max={max}
          step={step}
          value={from}
          onChange={(e) => onFromChange(Number(e.target.value))}
        />
        <input
          aria-label={`${label} to`}
          className={`${styles.thumb} ${styles.thumbRight}`}
          type="range"
          min={min}
          max={max}
          step={step}
          value={to}
          onChange={(e) => onToChange(Number(e.target.value))}
        />
      </div>
      <div className={styles.scale}>
        <span>{min}{unit}</span>
        <span>{max}{unit}</span>
      </div>
    </div>
  );
}
