import styles from "./Status.module.css";
import StatusDate from "./StatusDate";
import SubStatusList from "./SubStatusList";
import StatusName from "./StatusName";
import StatusGrid from "./StatusGrid";
import { useState } from "react";
import { CSSTransition } from "react-transition-group";
import "./Status.css";

function Status(props) {
  const subs = props.subcomponents ? props.subcomponents : [];
  const date = typeof props.date === Date ? props.date : new Date(props.date);
  const [expanded, setexpanded] = useState(false);
  const substatus =
    expanded && subs ? (
      <CSSTransition
        in={expanded}
        classNames={{
          appear: "my-appear",
          appearActive: "my-active-appear",
          appearDone: "my-done-appear",
          enter: "my-enter",
          enterActive: "my-active-enter",
          enterDone: "my-done-enter",
          exit: "my-exit",
          exitActive: "my-active-exit",
          exitDone: "my-done-exit",
        }}
        timeout={300}
        unmountOnExit
      >
        <StatusGrid style={{ width: "fit-content" }} statuses={subs} />
      </CSSTransition>
    ) : (
      <SubStatusList
        clickHandler={() => setexpanded(!expanded)}
        // clickHandler={() => console.log("you clicked the list")}
        statuses={props.subcomponents}
      />
    );
  const collapseButton = expanded ? (
    // <div className={styles.border}>
      <button className={styles.button} onClick={() => setexpanded(!expanded)}>
        collapse
      </button>
    // </div>
  ) : null;

  const style = !expanded ? styles.status : styles.status_expanded;
  const top_row_style = !expanded ? styles.status_top_row : styles.status_top_row_expanded;
  return (
    <div className={style}>
      <div className={top_row_style}>
        <div className={styles.status_name}>
          <StatusName name={props.name} details={props.details} />
        </div>
        <div className={style.status_date}>
          <StatusDate
            clickHandler={setexpanded}
            config={props.config}
            statusMessage={props.status_message}
            date={date}
            color={props.status}
          />
        </div>
        {collapseButton}
      </div>
      {/* <div className={styles.break} /> */}
      {/* <SubStatusList statuses={props.subcomponents} /> */}
      <div className={styles.status_sub_list}>{substatus}</div>
      {/* <StatusGrid statuses={subs} /> */}
    </div>
  );
}

export default Status;
