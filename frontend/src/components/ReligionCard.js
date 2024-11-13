import React from 'react';

function ReligionCard({ religion }) {
    return (
        <div className="card h-100 shadow-sm">
            <div className="card-body">
                <h3 className="card-title">{religion.name}</h3>
                <p className="card-text">{religion.description}</p>
                <div className="row mt-3">
                    <div className="col-md-6">
                        <h6>Sacred Texts:</h6>
                        <ul className="list-group list-group-flush">
                            {religion.sacred_texts.map((text, index) => (
                                <li key={index} className="list-group-item">{text}</li>
                            ))}
                        </ul>
                    </div>
                    <div className="col-md-6">
                        <h6>Practices:</h6>
                        <ul className="list-group list-group-flush">
                            {religion.practices.map((practice, index) => (
                                <li key={index} className="list-group-item">{practice}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ReligionCard;