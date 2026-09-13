import React from 'react';
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-c';
import 'prismjs/themes/prism-tomorrow.css';

interface CodeEditorProps {
    code: string;
    onChange: (code: string) => void;
    readOnly?: boolean;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({ code, onChange, readOnly }) => {
    return (
        <div className="font-mono text-sm border border-gray-700 rounded overflow-hidden bg-[#1e1e1e] shadow-lg">
            <div className="bg-gray-800 px-4 py-1 text-xs text-gray-400 border-b border-gray-700 flex justify-between items-center">
                <span>main.c</span>
                <span className="text-green-500">● Ready</span>
            </div>
            <Editor
                value={code}
                onValueChange={onChange}
                highlight={code => highlight(code, languages.c, 'c')}
                padding={16}
                style={{
                    fontFamily: '"Fira Code", "Fira Mono", monospace',
                    fontSize: 14,
                    backgroundColor: '#1e1e1e',
                    color: '#d4d4d4',
                    minHeight: '300px',
                }}
                disabled={readOnly}
                className="min-h-[300px] focus:outline-none"
                textareaClassName="focus:outline-none"
            />
        </div>
    );
};
