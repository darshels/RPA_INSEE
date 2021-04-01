import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { handleResponse } from './helpers';
import spinner from './Spinner.gif';
import './FormDeces.css';



class FormDeces extends React.Component{
    constructor(props) {
        super(props);
     
        this.state = {
          nom: "",
          prenom:"",
          dateNaissance:"",
          deces:"",
          loading:false
        };

        this.handleSubmitForm = this.handleSubmitForm.bind(this);
        this.handleChangeLastName = this.handleChangeLastName.bind(this);
        this.handleChangeFirstName = this.handleChangeFirstName.bind(this);
        this.handleChangeDateNaissance = this.handleChangeDateNaissance.bind(this);
      }

      getDeces(){
        fetch('https://rparecherchedeces.herokuapp.com/deces', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*'
          },
          body: JSON.stringify({
            nom: this.state.nom,
            prenom: this.state.prenom,
            dateNaissance: this.state.dateNaissance
          })
        }).then(handleResponse)
          .then((result) => {
            this.setState({deces: result.deces});
            this.setState({loading: false});
        }).catch((err) => {
            console.log(err);
            this.setState({loading: false});
        });
      }
     
      handleSubmitForm(event) {
        event.preventDefault();
        this.setState({loading: true});
        this.getDeces();
      }
     
      handleChangeLastName(event) {
        var value = event.target.value;
     
        this.setState({nom: value});
        this.setState({deces: ""});
      }

      handleChangeFirstName(event) {
        var value = event.target.value;
     
        this.setState({prenom: value});
        this.setState({deces: ""});
      }

      handleChangeDateNaissance(event) {
        var value = event.target.value;
     
        this.setState({dateNaissance: value});
        this.setState({deces: ""});
      }
     
      render() {
        
        let decesinfo

        if (this.state.deces === "nondeces") {
          decesinfo = 
          <div>
              <label>Nom : {this.state.nom}</label><br />
              <label>Prénom : {this.state.prenom}</label><br />
              <label>Date de Naissance : {this.state.dateNaissance}</label><br />
              <span className="badge badge-primary">Non décédé</span>
            </div>;
        } else if (this.state.deces !== "") {
          decesinfo = 
            <div>
              <label>Nom : {this.state.nom}</label><br />
              <label>Prénom : {this.state.prenom}</label><br />
              <label>Date de Naissance : {this.state.dateNaissance}</label> <br />           
              <label>Date de décès : {this.state.deces}</label><br />
              <span className="badge badge-secondary">Décédé</span>
            </div>;
        }

        return (
          <div>
            {this.state.loading ? (
              <div class="divmiddle"><img src={spinner} alt="loading..." /></div>) : (
                ""
              ) 
            }
            <h2 class="text-center">Recherche des personnes décédées</h2>
            
            <form onSubmit={event => this.handleSubmitForm(event)}>
                <div className="form-group">
                  <label>Nom :</label>
                  <input
                      type="text"
                      value={this.state.nom}
                      required="required"
                      className="form-control"
                      onChange={event => this.handleChangeLastName(event)}
                  />
                </div>
                <div className="form-group">
                  <label>Prénom :</label>
                  <input
                      type="text"
                      value={this.state.prenom}
                      required="required"
                      className="form-control"
                      onChange={event => this.handleChangeFirstName(event)}
                  />
                </div>
                <div className="form-group">
                  <label>Date de naissance :</label>
                  <input
                      required="required"
                      min="1900-01-01" max="2022-01-01"
                      className="form-control" type="date"
                      onChange={event => this.handleChangeDateNaissance(event)}
                  />
                </div>
                {this.state.loading ? (
                  <input type="submit" value="Submit" className="btn btn-primary" disabled/>) : (
                    <input type="submit" value="Submit" className="btn btn-primary"/>
                  ) 
                }
            </form>
            <div>
              <br />
              {decesinfo}            
            </div>
          </div>
        );
      }
    }

export default FormDeces;
