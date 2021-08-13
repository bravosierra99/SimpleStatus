import styles from "./Status.module.css";
import StatusDate from "./StatusDate";
import SubStatusList from "./SubStatusList";
import StatusName from "./StatusName";
import StatusGrid from "./StatusGrid";
import { useState } from "react";


function Status(props) {
  const subs = props.subcomponents ? props.subcomponents : [];
  const [expanded, setexpanded] = useState(false);
  console.log("expanded & subs")
  const substatus =
    expanded && subs ? (
      <StatusGrid style={{ width: "100%" }} statuses={subs} />
    ) : (
      <SubStatusList
        clickHandler={() => setexpanded(!expanded)}
        // clickHandler={() => console.log("you clicked the list")}
        statuses={props.subcomponents}
      />
    );
    console.log(expanded)
    const collapseButton = expanded ? <div className={styles.border}><button className={styles.button} onClick={()=>setexpanded(!expanded)}>collapse</button></div> : null
  return (
    <div className={styles.border}>
      {/* <div className={styles.status}> */}
      <div style={{ width: "100%" }} className={styles.status}>
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
