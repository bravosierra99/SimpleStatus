// import logo from "./logo.svg";
import "./App.css";
import StatusGrid from "./components/Status/StatusGrid";

const today = new Date();
const outside_of_timeout = new Date(today);

// const today = "today";
// const yesterday = "yesterday";

outside_of_timeout.setDate(outside_of_timeout.getDate() - 1.5);

outside_of_timeout.setTime(outside_of_timeout.getTime() - 1000 * 60 * 82);

const DUMMY_SUB_SUBCOMPONENTS = [
  {
    name: "subsubcomponent1",
    details:
      "I am the subsubcomponent, if I'm green then the following is true",
    date: today,
    status: "green",
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },
    status_message: "Completed Run",
    key: "comp1.subcomp1",
  },
  {
    name: "subsubcomponent2",
    details:
      "I am the subsubcomponent, if I'm green then the following is true",
    date: today,
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },
    status: "green",
    status_message: "Completed Run",
    key: "comp1.subcomp2",
  },
];

const DUMMY_SUBCOMPONENTS = [
  {
    name: "subcomponent1",
    details: "I am the subcomponent, if I'm green then the following is true",
    date: today,
    status: "green",
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },
    status_message: "Completed Run",
    subcomponents: DUMMY_SUB_SUBCOMPONENTS,
    key: "comp1.subcomp1",
  },
  {
    name: "subcomponent2",
    details: "I am the subcomponent, if I'm green then the following is true",
    date: today,
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },
    status: "green",
    status_message: "Completed Run",
    key: "comp1.subcomp2",
  },
  {
    name: "subcomponent3",
    details: "I am the subcomponent, if I'm green then the following is true",
    date: today,
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },
    status: "red",
    status_message: "Failed to twiddle the thingamabob",
    key: "comp1.subcomp3",
  },
  // {
  //     name: "subcomponent3",
  //     details: "I am the subcomponent, if I'm green then the following is true",
  //     date: today,
  //     config: {
  //       timeout_min: 1234,
  //       timeout_color: "yellow",
  //     },
  //     status: "red",
  //     status_message: "Failed to twiddle the thingamabob",
  //     key: "comp1.subcomp3",
  //   },
];
const DUMMY_STATUSES = [
  {
    name: "component1",
    details: "I am the component blah, if I'm green then the following is true",
    date: today,
    status: "green",
    status_message: "Completed Run",
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },
    key: "comp1",
    subcomponents: DUMMY_SUBCOMPONENTS,
  },
  {
    name: "component2_thegreatestcomponent",
    details: "I am the component blah, if I'm green then the following is true",
    date: outside_of_timeout,
    status: "green",
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },
    status_message: "Completed Run",
    key: "comp2",
  },
  {
    name: "component3",
    details: "I am the component blah, if I'm green then the following is true",
    date: today,
    status: "red",
    status_message: "Failed to twiddle the thingamabob",
    subcomponents:DUMMY_SUBCOMPONENTS,
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },
    key: "comp3",
  },
  {
    name: "component4",
    details: "I am the component blah, if I'm green then the following is true",
    date: outside_of_timeout,
    status: "red",
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },

    status_message: "Failed to twiddle the thingamabob",
    key: "comp4",
  },
  {
    name: "component5",
    details: "I am the component blah, if I'm green then the following is true",
    date: today,
    status: "yellow",
    config: {
      timeout_min: 1234,
      timeout_color: "yellow",
    },
    status_message: "warnings",
    key: "comp5",
  },
];

function App() {
  return (
    <div>
      <h2>Simple Status Server (Keep it Simple, Stupid)</h2>
      <StatusGrid statuses={DUMMY_STATUSES} />
    </div>
  );
}

export default App;
