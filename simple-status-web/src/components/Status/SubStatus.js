import styles from "./SubStatus.module.css";

function SubStatus(props) {
  return (
    <div className={styles.border}>
      <div
        className={styles.subStatus}
        style={{ backgroundColor: props.color }}
      ></div>
    </div>
  );
}

export default SubStatus;
