import logo from "./logo.svg";
import "./App.css";
import StatusGrid from "./components/Status/StatusGrid";

const today = new Date();
const yesterday = new Date(today);

// const today = "today";
// const yesterday = "yesterday";

yesterday.setDate(yesterday.getDate() - 1.5);
yesterday.setTime(yesterday.getTime() - 1000 * 60 * 82);
const DUMMY_SUBCOMPONENTS = [
  {
    name: 'subcomponent1',
    date: today,
    status: "green",
    key: 'comp1.subcomp1',
  },
  {
    name: 'subcomponent2',
    date: today,
    status: "red",
    key: 'comp1.subcomp2',
  },

];
const DUMMY_STATUSES = [
  { name: "component1", date: today, status: "green", key: "comp1", subcomponents: DUMMY_SUBCOMPONENTS },
  {
    name: "component2",
    date: yesterday,
    status: "red",
    key: "comp2",
  },
];


function App() {
  return (
    <div>
      <h2>Simple Status Server</h2>
      <StatusGrid statuses={DUMMY_STATUSES} />
    </div>
  );
}

export default App;
