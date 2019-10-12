import React, { Component } from 'react'

const initialState = {
    "search": ""
}
export default class Login extends Component {
    constructor(props) {
        super(props)

        this.state = initialState

        this.inputChange = this.inputChange.bind(this)
        this.search = this.search.bind(this)
    }

    inputChange(e) {
        if (e.target.id == "search") {
            this.setState({"search": e.target.value})
        }
    }

    search() {
        alert(this.state.search)
    }

    render() {
        return (
            <div className="main">
                <div className="search">
                    <input onChange={this.inputChange} type="text" id="search" className="form-control" placeholder="Digite um bairro..."></input>
                    <button onClick={this.search} className="btn btn-lg btn-primary">Pesquisar</button>
                </div>
            </div>
        )
    }
}