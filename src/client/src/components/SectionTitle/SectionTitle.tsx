import styles from './SectionTitle.module.css';

type Props = { children: React.ReactNode };

export default function SectionTitle({ children }: Props) {
  return <h3 className={styles.title}>{children}</h3>;
}
