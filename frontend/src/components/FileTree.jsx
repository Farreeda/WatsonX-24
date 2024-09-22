import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const FileTreeNode = ({ file, path, onSendFilePath, onExpand }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [children, setChildren] = useState([]);

  const toggleExpand = async () => {
    if (!isExpanded) {
      try {
        const response = await axios.get(`http://localhost:5000/get-file-tree`, { params: { path: `${path}\\${file}` } });
        setChildren(response.data);
      } catch (error) {
        console.error('Error fetching child files:', error);
      }
    }
    setIsExpanded(!isExpanded);
  };

  return (
    <li className="list-group-item">
      <div className="d-flex justify-content-between align-items-center">
        
        <span onClick={toggleExpand} style={{ cursor: 'pointer' }}>
          {file} {isExpanded ? '-' : '+'}
        </span>
        <button className="btn btn-secondary btn-sm" onClick={() => onSendFilePath(`${path}\\${file}`)}>
          Send Path
        </button>
      </div>
      {isExpanded && children.length > 0 && (
        <ul className="list-group mt-2">
          {children.map((child, index) => (
            <FileTreeNode
              key={index}
              file={child}
              path={`${path}\\${file}`}
              onSendFilePath={onSendFilePath}
              onExpand={onExpand}
            />
          ))}
        </ul>
      )}
    </li>
  );
};

const FileTree = () => {
  const [path, setPath] = useState("C:\\Users\\Hamza\\Downloads");
  const [files, setFiles] = useState([]);

  const fetchFileTree = async (directory) => {
    try {
      const response = await axios.get(`http://localhost:5000/get-file-tree`, { params: { path: directory } });
      setFiles(response.data);
    } catch (error) {
      console.error('Error fetching file tree:', error);
    }
  };

  const handlePathChange = (e) => {
    setPath(e.target.value);
  };

  const handleFetchFiles = () => {
    fetchFileTree(path);
  };

  const handleSendFilePath = async (filePath) => {
    try {
      await axios.post('http://localhost:5000/send-file-path', { filePath });
      alert(`File path sent: ${filePath}`);
    } catch (error) {
      console.error('Error sending file path:', error);
    }
  };

  useEffect(() => {
    fetchFileTree(path);
  }, [path]);

  return (
    <div className="container mt-4">
      <h2>File Tree Viewer</h2>
      <div className="mb-3">
        <input
          type="text"
          className="form-control"
          value={path}
          onChange={handlePathChange}
          placeholder="Enter directory path"
        />
        <button className="btn btn-primary mt-2" onClick={handleFetchFiles}>
          Load Files
        </button>
      </div>
      <ul className="list-group">
        {files.map((file, index) => (
          <FileTreeNode
            key={index}
            file={file}
            path={path}
            onSendFilePath={handleSendFilePath}
          />
        ))}
      </ul>
    </div>
  );
};

export default FileTree;
