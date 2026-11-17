import React, { useState, useEffect } from 'react';

// 1. Mock dataset
const MOCK_ITEMS = [
  'Apple',
  'Apricot',
  'Avocado',
  'Banana',
  'Blackberry',
  'Blueberry',
  'Cherry',
  'Coconut',
  'Cranberry',
  'Date',
  'Dragonfruit',
  'Elderberry',
  'Fig',
  'Grape',
  'Grapefruit',
  'Guava',
  'Honeydew',
  'Kiwi',
  'Lemon',
  'Lime',
  'Mango',
  'Orange',
  'Papaya',
  'Peach',
  'Pear',
  'Pineapple',
  'Raspberry',
  'Strawberry',
  'Watermelon',
];

// 2. Mock API that simulates latency and honors AbortSignal
const mockSearchApi = (query, { signal, delay = 800 } = {}) => {
  return new Promise((resolve, reject) => {
    // If the signal was already aborted before calling
    if (signal?.aborted) {
      return reject(new DOMException('The user aborted a request.', 'AbortError'));
    }

    // Simulate network delay
    const timer = setTimeout(() => {
      const filtered = MOCK_ITEMS.filter((item) =>
        item.toLowerCase().includes(query.toLowerCase())
      );
      resolve(filtered);
    }, delay);

    // Cancel and clean up if aborted during the delay
    signal?.addEventListener(
      'abort',
      () => {
        clearTimeout(timer);
        reject(new DOMException('The user aborted a request.', 'AbortError'));
      },
      { once: true }
    );
  });
};

const styles = {
  main: {
    padding: '24px',
    maxWidth: '480px',
    fontFamily: 'system-ui, sans-serif',
  },
  title: {
    color: '#5C6AC4',
    marginBottom: '16px',
  },
  input: {
    width: '100%',
    padding: '10px 12px',
    fontSize: '16px',
    boxSizing: 'border-box',
    borderRadius: '6px',
    border: '1px solid #ccc',
  },
  status: {
    color: '#666',
    fontSize: '14px',
    margin: '12px 0 0',
  },
  list: {
    listStyle: 'none',
    padding: 0,
    marginTop: '16px',
    border: '1px solid #eee',
    borderRadius: '6px',
    overflow: 'hidden',
  },
  listItem: {
    padding: '10px 12px',
    borderBottom: '1px solid #eee',
  },
};

function App() {
  const [searchText, setSearchText] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const query = searchText.trim();

    if (!query) {
      setSearchResults([]);
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    const controller = new AbortController();

    // 400ms debounce before invoking the mock API
    const timerId = setTimeout(async () => {
      try {
        const results = await mockSearchApi(query, {
          signal: controller.signal,
          delay: 700, // 700ms simulated server latency
        });
        setSearchResults(results);
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Search error:', err);
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      }
    }, 400);

    return () => {
      clearTimeout(timerId);
      controller.abort();
    };
  }, [searchText]);

  return (
    <div style={styles.main}>
      <h2 style={styles.title}>Fruit Search (Mocked API)</h2>
      <input
        style={styles.input}
        type="text"
        placeholder="Type to search (e.g. 'ap', 'berry')..."
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
      />

      {isLoading && <p style={styles.status}>Searching...</p>}

      {!isLoading && searchText && searchResults.length === 0 && (
        <p style={styles.status}>No matching results found.</p>
      )}

      {searchResults.length > 0 && (
        <ul style={styles.list}>
          {searchResults.map((item) => (
            <li key={item} style={styles.listItem}>
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;