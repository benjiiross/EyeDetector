import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import DownloadIcon from "./DownloadIcon";
import Popup from "./Popup";

interface CustomFile extends File {
  preview: string;
}

export default function ImageDropzone() {
  const [file, setFile] = useState<CustomFile | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [apiResponse, setApiResponse] = useState([]);

  // useCallback is used to prevent the function from being recreated on every render
  const onDrop = useCallback((acceptedFile: File[]) => {
    if (acceptedFile.length === 0) {
      return;
    }
    const customFile = acceptedFile[0] as CustomFile;
    Object.assign(customFile, {
      preview: URL.createObjectURL(acceptedFile[0]),
    });
    setFile(customFile);
  }, []);

  // useDropzone is a React hook that exposes the functionality of the Dropzone library
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/jpeg": [".jpg", ".jpeg"],
      "image/png": [".png"],
    },
    maxSize: 6 * 1024 * 1024,
    multiple: false,
    onDropRejected: () => {
      alert("Please upload an image file with max size of 6MB");
    },
  });

  // This function is called when the user clicks the "Upload" button
  const handleUpload = async () => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", file as Blob);

    const response = await fetch(
      "https://eyedetector-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/1f803d80-78d5-4291-b386-89353c0ce67f/classify/iterations/Iteration1/image",
      {
        method: "POST",
        headers: {
          "Prediction-Key": "2a530a0870d04fde9dbd1277358e0608",
        },
        body: formData,
      }
    );

    const data = await response.json();
    console.log(data);
    setApiResponse(data.predictions);
    setIsLoading(false);
    setIsOpen(true);
  };

  return (
    <div className="flex flex-col items-center justify-center h-full">
      {isOpen && (
        <Popup apiResponse={apiResponse} handleClose={() => setIsOpen(false)} />
      )}
      <form className="w-full max-w-lg">
        <div
          {...getRootProps()}
          className="bg-green-200 text-center bg-opacity-80 px-5 py-20 transition duration-200 border-dashed hover:cursor-pointer border-2 border-black hover:border-sky-500 mx-4 sm:mx-8 md:mx-16 lg:mx-24 rounded-3xl flex items-center justify-center"
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

        {file && (
          <div className="my-10 space-y-4">
            <div className="flex flex-col justify-center items-center space-y-2">
              <img
                src={file.preview}
                alt={file.name}
                className="w-40 h-40 object-cover rounded-lg"
              />
              <span className="text-sm font-semibold">{file.name}</span>
            </div>
            <button
              type="button"
              className="bg-green-500 text-white px-5 py-2 rounded-lg shadow-lg hover:bg-green-600 transition duration-200 active:bg-green-700"
              onClick={handleUpload}
              disabled={isLoading}
            >
              {isLoading ? (
                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647zM12 20.373V24c4.418 0 8-3.582 8-8h-4a4 4 0 00-8 0v4.373l-4.243-4.243a1 1 0 00-1.414 1.414L10.586 18H8a4 4 0 004 4z"
                  />
                </svg>
              ) : (
                "Upload"
              )}
            </button>
          </div>
        )}
      </form>
    </div>
  );
}
