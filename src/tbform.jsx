var React = require('react');
var ReactDOM = require('react-dom');

var Diagnosis = React.createClass({
  onChange: function(event) {
    if (event.target.value == "Negative TB") {
      this.setState({showStatus: false});
    } else {
      this.setState({showStatus: true});
    }
  },
  getInitialState: function() {
    return {
      showStatus: true
    }
  },
  render: function() {
    return (
      <div>
        <div className="form-group">
          <label htmlFor="address">Diagnosis</label>
          <select className="form-control" onChange={this.onChange}>
            <option>Suspect TB</option>
            <option>Confirm positive TB</option>
            <option>Negative TB</option>
          </select>
        </div>
        { this.state.showStatus ? <PatientStatus /> : null }
      </div>
    );
  }
});

var PatientStatus = React.createClass({
  render: function() {
    return (<div className="form-group">
        <label htmlFor="address">TB Patient Status</label>
        <select className="form-control">
          <option>New</option>
          <option>Chronic</option>
          <option>Relapse</option>
          <option>Drop out</option>
        </select>
      </div>
    );
  }
});

ReactDOM.render(<Diagnosis/>, document.getElementById('diagnosis'));