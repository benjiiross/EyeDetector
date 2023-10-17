import { useDropzone } from "react-dropzone";
import DownloadIcon from "./DownloadIcon";
import { useCallback } from "react";
import { useState } from "react";

export default function ImageDropzone() {
  const [file, setFile] = useState<File[]>([]);
  const onDrop = useCallback((acceptedFile: File[]) => {
    if (acceptedFile?.length === 0) {
      return;
    }

    setFile((previousFile) => [
      Object.assign(acceptedFile[0], {
        preview: URL.createObjectURL(acceptedFile[0]),
      }),
    ]);

    console.log(acceptedFile);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ".jpg, .jpeg, .png",
    maxSize: 6 * 1024 * 1024, // 6MB
    multiple: false,
  });

  return (
    <form action="/api/eye" method="POST" encType="multipart/form-data">
      <div
        {...getRootProps()}
        className="bg-green-200 text-center bg-opacity-80 px-5 py-40 transition duration-200 border-dashed hover:cursor-pointer border-2 border-black hover:border-sky-500 mx-40 rounded-3xl flex items-center justify-center"
      >
        <input {...getInputProps()} />
        <div className="flex items-center justify-center">
          <DownloadIcon />
          {isDragActive ? (
            <p className="ml-2">Drop the file here ...</p>
          ) : (
            <p className="ml-2">
              Drag & drop a file here, or click to select a file
            </p>
          )}
        </div>
      </div>

      {/* preview */}
      <div className="flex justify-center items-center space-x-2 mt-10">
        {file.map((file) => (
          <div
            key={file.name}
            className="flex flex-col justify-center items-center space-y-2"
          >
            <img
              src={file.preview}
              alt={file.name}
              className="w-40 h-40 object-cover rounded-lg"
            />
            <span className="text-sm font-semibold">{file.name}</span>
          </div>
        ))}
      </div>
    </form>
  );
}
