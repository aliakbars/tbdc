// var React = require('react');
// var ReactDOM = require('react-dom');

var Drug = React.createClass({
  render: function() {
    var options = [];
    var freq_week = [];
    for (var i = 1; i <= 7; i++) {
      options.push(<option key={i} value="{i}">{i}/day</option>);
      freq_week.push(<option key={i} value="{i}">{i} days/week</option>);
    }
    if (this.props.index != 0) {
        var deleteButton = (<div className="form-group col-xs-1">
        <label>&nbsp;</label>
        <div className="input-group">
          <span className="btn btn-danger" onClick={this.props.deleteTask}>Delete</span>
        </div>
      </div>);
    } else {
        var deleteButton = (<div className="form-group col-xs-1"></div>);
    }
    return (<div className="row">
      <div className="form-group col-md-2">
        <label htmlFor="medication[]">Medication</label>
        <select className="form-control" name="medication[]">
          <option value="HRZE">FDC 4 combination (HRZE)</option>
          <option value="HR">FDC 2 combination (HR)</option>
          <option value="H">Isoniazid (H)</option>
          <option value="R">Rifampisin (R)</option>
          <option value="Z">Pirazinamid (Z)</option>
          <option value="E">Etambutol (E)</option>
          <option value="S">Streptomisin (S)</option>
          <option value="HRZ">FDC for children (HRZ)</option>
          <option value="Km">Kanamysin (Km)</option>
          <option value="Cm">Capreomysin (Cm)</option>
          <option value="Lfx">Levofloksasin (Lfx)</option>
          <option value="Mfx">Moksifloksasin (Mfx)</option>
          <option value="Etio">Ethionamide (Etio)</option>
          <option value="Cs">Cycloserine (Cs)</option>
          <option value="PAS">Para-aminosalicyclic Acid (PAS)</option>
        </select>
      </div>
      <div className="form-group col-md-2">
        <label htmlFor="dosage[]">Dose</label>
        <div className="input-group">
          <input type="text" className="form-control" id="" name="dosage[]" placeholder=""/>
          <span className="input-group-addon">mg/kg weight</span>
        </div>
      </div>
      <div className="form-group col-md-1">
        <label htmlFor="freq_day[]">Frequency</label>
        <select className="form-control" name="freq_day[]">
          {options}
        </select>
      </div>
      <div className="form-group col-md-2">
        <label htmlFor="freq_week[]">&nbsp;</label>
        <select className="form-control" name="freq_week[]">
          {freq_week}
        </select>
      </div>
      <div className="form-group col-md-2">
        <label htmlFor="start_date[]">Start date</label>
        <input type="text" className="form-control" id="" name="start_date[]" placeholder="YYYY-MM-DD"/>
      </div>
      <div className="form-group col-md-2">
        <label htmlFor="end_date[]">Expected end date</label>
        <input type="text" className="form-control" id="" name="end_date[]" placeholder="YYYY-MM-DD"/>
      </div>
      {deleteButton}
    </div>
    );
  }
});

var DrugList = React.createClass({
    addNewDrug: function(event) {
        this.setState({
            drugs: this.state.drugs + 1
        });
    },
    deleteTask: function(event) {
        this.setState({
            drugs: this.state.drugs - 1
        });
    },
    getInitialState: function() {
        return {
            drugs: 1
        }
    },
    render: function() {
        var drugs = [];
        for (var i = 0; i < this.state.drugs; i++) {
            drugs.push(<Drug key={i} index={i} deleteTask={this.deleteTask} />);
        }
        return (<div>
            {drugs}
            <span className="btn btn-default btn-sm" id="add-treatment" onClick={this.addNewDrug}>Add another</span>
        </div>
        );
    }
});

ReactDOM.render(<DrugList/>, document.getElementById('drugs'));