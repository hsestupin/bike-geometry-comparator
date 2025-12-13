import styles from './BrandFilter.module.css';
import Checkbox from '@/components/Checkbox/Checkbox';

type Props = {
  brands: string[];
  selected: Set<string>;
  onToggle: (brand: string) => void;
};

export default function BrandFilter({ brands, selected, onToggle }: Props) {
  return (
    <div className={styles.wrap}>
      <div className={styles.headerOnly}>
        <span className={styles.title}>Brands</span>
      </div>
      <ul className={styles.list}>
        {brands.map(brand => (
          <li key={brand} className={styles.item}>
            <Checkbox
              label={brand}
              checked={selected.has(brand)}
              onChange={() => onToggle(brand)}
            />
          </li>
        ))}
      </ul>
    </div>
  );
}
