import { useId } from 'react';
import styles from './Checkbox.module.css';

type Props = {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
};

export default function Checkbox({ label, checked, onChange }: Props) {
  const id = useId();
  return (
    <div className={styles.wrap}>
      <input
        id={id}
        type="checkbox"
        className={styles.box}
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
      />
      <label className={styles.label} htmlFor={id}>{label}</label>
    </div>
  );
}
