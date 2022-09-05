import styles from "./SubStatus.module.css";
import { timed_out } from "./StatusDate";

function SubStatus(props) {
  const date = typeof props.date === Date ? props.date : new Date(props.date);
  const timed_out_result = timed_out(date, props.config.timeout_min);
  //TODO this is specific to only having 3 colors... which is dangerous if you make changes in the future.  Really we just want to check that we don't time-out and go "up" a color... which should be checkable
  const color =
    timed_out_result && (props.color === "green" || props.color === "yellow")
      ? props.config.timeout_color
      : props.color;
  return (
    <div className={styles.border}>
      <div
        className={styles.subStatus}
        style={{ backgroundColor: color }}
      ></div>
    </div>
  );
}

export default SubStatus;
