importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.1/full/pyodide.js");

let pyodideInstance = null;

async function initPyodide(){
    self.postMessage({type:"status", data:"starting engine.."})
    const py = await loadPyodide();

    await py.loadPackage("micropip");

    await py.runPythonAsync(`
        import micropip
        await micropip.install('python-chess')
    `);
    
    await py.runPythonAsync(`
        import os
        os.makedirs('pyngin', exist_ok=True)
    `);

    const files = [
        { url: '/engine/pyngin/__init__.py', path: 'pyngin/__init__.py' },
        { url: '/engine/pyngin/board.py', path: 'pyngin/board.py' },
        { url: '/engine/pyngin/moves.py', path: 'pyngin/moves.py' },
        { url: '/engine/pyngin/converter.py', path: 'pyngin/converter.py' },
        { url: '/engine/pyngin/engine.py', path: 'pyngin/engine.py' },
        { url: '/engine/pyngin/evaluate.py', path: 'pyngin/evaluate.py' },
        { url: '/engine/pyngin/pieces.py', path: 'pyngin/pieces.py' },
        { url: '/engine/wrapper.py', path: 'wrapper.py' },
    ];

    for (const file of files) {
        const res = await fetch(file.url);
        const code = await res.text();
        py.FS.writeFile(file.path, code);
    }

    await py.runPythonAsync(`import wrapper`);
    pyodideInstance = py;
    self.postMessage({type:"ready"});
}

initPyodide();

self.onmessage = async function(e) {
    const {type, fen, depth} = e.data;
    if (type == "search" && pyodideInstance) {
        try {
            const move = await pyodideInstance.runPythonAsync(`wrapper.get_best_move("${fen}", ${depth})`);
            self.postMessage({type:"move", data:move});
        }
        catch (error){
            self.postMessage({type:'error', data:error.toString()});
        }
    }
};