import React from "react"
import 'bootstrap/dist/css/bootstrap.min.css'

import Header from "./header"
import Body from "./body"

export default props => (
    <div className="container">
        <Header />
        <Body />
    </div>
)