import React from 'react'
import { Block } from 'baseui/block'

function Main(props) {

    

    return(
        <Block className='main'>
            {props.children}
        </Block>
    )

}

export default Main