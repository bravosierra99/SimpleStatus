import styles from "./SubStatusList.module.css";
import SubStatus from "./SubStatus";

function SubStatusList(props) {
  const statuses = props.statuses ? (
    props.statuses.map((status) => (
      <SubStatus key={status.key} color={status.status} />
    ))
  ) : (
    <div></div>
  );

  return <div onClick={props.clickHandler} className={styles.substatus_list}>{statuses}</div>;
}

export default SubStatusList;
