var React = require('react');
var ReactDOM = require('react-dom');

var Drug = React.createClass({
  render: function() {
    var options = [];
    for (var i = 1; i <= 7; i++) {
      options.push(<option key={i} value="{i}">{i} times a week</option>);
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
      <div className="form-group col-xs-4">
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
      <div className="form-group col-xs-4">
        <label htmlFor="doses[]">Doses</label>
        <div className="input-group">
          <input type="text" className="form-control" id="" name="doses[]" placeholder=""/>
          <span className="input-group-addon">mg/kg weight</span>
        </div>
      </div>
      <div className="form-group col-xs-3">
        <label htmlFor="frequency[]">Frequency</label>
        <select className="form-control" name="frequency[]">
          {options}
        </select>
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