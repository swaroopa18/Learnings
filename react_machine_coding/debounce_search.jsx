import React from 'react';
import { useState, useEffect, useMemo } from 'react'

function App() {
    const [searchText, setSearchText] = useState('')

    const styles = {
        main: {
            padding: '20px',
        },
        title: {
            color: '#5C6AC4'
        },
    };

    const debounce = (fn, delay) => {
        let timerId;
        const debounced = (...args) => {
            clearTimeout(timerId)
            timerId = setTimeout(() => fn(...args), delay)
        }
        debounced.cancel = () => clearTimeout(timerId)
        return debounced
    }

    const handleSearch = (value) => {
        console.log("search", value)
    }


    // without use memo debounce will get reset after search text change and timerid also get reset and it wont work as expected
    const debounceSearch = useMemo(
        () => debounce(handleSearch, 1000),
        []
    );

    useEffect(() => {
        debounceSearch(searchText)

        return (() => debounceSearch.cancel())
    }, [searchText, debounceSearch])

    return (
        <div style={styles.main}>
            <h2>Search Results</h2>
            <input value={searchText} onChange={(event) => setSearchText(event.target.value)} />
        </div>
    )
}

export default App