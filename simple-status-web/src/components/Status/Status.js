import styles from "./Status.module.css";
import StatusDate from "./StatusDate";
import SubStatusList from "./SubStatusList";
import StatusName from "./StatusName";

function clickHandler(){
  console.log("you clicked the date")
}

function Status(props) {
  console.log(props.subcomponents);
  return (
    <div className={styles.border}>
      <div className={styles.status}>
        <StatusName name={props.name} details={props.details}/>
        <StatusDate clickHandler={clickHandler} config={props.config} statusMessage={props.status_message} date={props.date} color={props.status} />
        <SubStatusList statuses={props.subcomponents} />
      </div>
    </div>
  );
}

export default Status;
