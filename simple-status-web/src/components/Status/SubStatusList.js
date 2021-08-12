import styles from "./SubStatusList.module.css";
import SubStatus from "./SubStatus";

function SubStatusList(props) {
  console.log(props.statuses);
  const statuses = props.statuses ? (
    props.statuses.map((status) => (
      <SubStatus key={status.key} color={status.status} />
    ))
  ) : (
    <div></div>
  );

  return <div className={styles.substatus_list}>{statuses}</div>;
}

export default SubStatusList;
