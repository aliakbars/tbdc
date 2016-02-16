var React = require('react');
var ReactDOM = require('react-dom');

var FilteredList = React.createClass({
  filterList: function(event){
    var updatedList = this.state.initialPatients;
    updatedList = updatedList.filter(function(patient){
      return patient.name.toLowerCase().search(
        event.target.value.toLowerCase()) !== -1;
    });
    this.setState({patients: updatedList});
  },
  getInitialState: function(){
    return {
      initialPatients: [
        {
          "birthdate": "1969-04-11",
          "gender": "M",
          "identifier": "A110",
          "name": "Joe Blitzstein"
        },
        {
          "birthdate": "1950-11-05",
          "gender": "M",
          "identifier": "A111",
          "name": "John Doe"
        },
        {
          "birthdate": "1969-06-22",
          "gender": "F",
          "identifier": "A112",
          "name": "Judy Garland"
        }
      ],
      patients: []
    }
  },
  componentWillMount: function(){
    this.setState({patients: this.state.initialPatients})
  },
  render: function(){
    return (
      <div>
        <form>
          <div className="form-group">
            <label htmlFor="query">Find patient(s)</label>
            <input type="text" className="form-control" id="query" placeholder="Search by ID or name" onChange={this.filterList} />
          </div>
        </form>
        <table className="table table-hover">
          <thead>
            <tr>
              <th>Identifier</th>
              <th>Name</th>
              <th>Gender</th>
              <th>Birthdate</th>
            </tr>
          </thead>
          <List patients={this.state.patients}/>
        </table>
      </div>
    );
  }
});

var List = React.createClass({
  render: function() {
    var patients = this.props.patients.map(function(patient) {
      return (<tr key={patient.identifier}>
        <td>{patient.identifier}</td>
        <td>{patient.name}</td>
        <td>{patient.gender}</td>
        <td>{patient.birthdate}</td>
      </tr>);
    });
    return (<tbody>
        {patients}
      </tbody>
    );
  }
});

ReactDOM.render(<FilteredList/>, document.getElementById('patient-list'));