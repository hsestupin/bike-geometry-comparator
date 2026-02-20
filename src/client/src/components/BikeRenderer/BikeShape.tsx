import {DEFAULT_GEOMETRY, Geometry} from "@/components/BikeRenderer/bikeGeometry";
import {renderBikeShapeSvg} from "@/components/BikeRenderer/bikeSvgRenderer";

import styles from './bikeShape.module.css';

type Props = {
  geometry?: Geometry;
  referenceGeometry?: Geometry;
};

export default function BikeShape(props: Props) {
  const {geometry = DEFAULT_GEOMETRY, referenceGeometry} = props;

  const foregroundHtml = renderBikeShapeSvg(geometry, {
    component: styles.component,
    dimLine: styles.dimLine,
    bar: styles.bar,
    forkFill: styles.forkFill,
    frameFill: styles.frameFill,
    joint: styles.joint,
    tire: styles.tire,
    rim: styles.rim,
    text: styles.text
  });

  if (!referenceGeometry) {
    return (
      <div
        className={styles.root}
        dangerouslySetInnerHTML={{__html: foregroundHtml}}
      />
    );
  }

  const ghostHtml = renderBikeShapeSvg(referenceGeometry, {
    component: styles.ghostComponent,
    dimLine: styles.ghostDimLine,
    bar: styles.ghostComponent,
    forkFill: styles.ghostFork,
    frameFill: styles.ghostFrame,
    joint: styles.ghostJoint,
    tire: styles.ghostTire,
    rim: styles.ghostRim,
    text: styles.ghostText,
  }, {showDimensions: false});

  return (
    <div className={`${styles.root} ${styles.overlay}`}>
      <div
        className={styles.ghostLayer}
        dangerouslySetInnerHTML={{__html: ghostHtml}}
      />
      <div
        style={{position: 'relative'}}
        dangerouslySetInnerHTML={{__html: foregroundHtml}}
      />
    </div>
  );
}
