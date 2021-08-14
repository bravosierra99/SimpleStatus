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
    <div className={styles.border}>
      <button className={styles.button} onClick={() => setexpanded(!expanded)}>
        collapse
      </button>
    </div>
  ) : null;
  return (
    <div className={styles.border}>
      {/* <div className={styles.status}> */}
      <div style={{ width: "fit-content" }} className={styles.status}>
        <StatusName name={props.name} details={props.details} />
        <StatusDate
          clickHandler={setexpanded}
          config={props.config}
          statusMessage={props.status_message}
          date={props.date}
          color={props.status}
        />
        {collapseButton}

        <div className={styles.break} />
        {/* <SubStatusList statuses={props.subcomponents} /> */}
        {substatus}
        {/* <StatusGrid statuses={subs} /> */}
      </div>
    </div>
  );
}

export default Status;
