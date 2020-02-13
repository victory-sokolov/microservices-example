import axios from "axios";
import React, { Component } from "react";
import ReactDOM from "react-dom";
import UsersList from "./components/UsersList";

class App extends Component {
  constructor() {
    super();
    this.state = {
      users: []
    };
  }

  componentDidMount() {
    this.getUsers();
  }

  getUsers() {
    axios
      .get("http://192.168.99.101:5001/users")
      .then(res => {
        this.setState({ users: res.data.data.users });
      })
      .catch(err => {
        console.log(err);
      });
  }

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-4">
            <br />
            <h1>All Users</h1>
            <hr />
            <br />
            <UsersList users={this.state.users} />
          </div>
        </div>
      </div>
    );
  }
}
ReactDOM.render(<App />, document.getElementById("root"));
