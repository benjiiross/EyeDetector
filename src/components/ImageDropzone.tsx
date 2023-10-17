import ImageDropzone from "react-dropzone";

export default function ImageDropzone() {
  return (
    <ImageDropzone onDrop={(acceptedFiles) => console.log(acceptedFiles)}>
      {({ getRootProps, getInputProps }) => (
        <section className="bg-green-200 text-center bg-opacity-50 p-5 transition duration-200 border-dashed hover:cursor-pointer border-2 border-green-200 hover:border-sky-500 mx-40 rounded-lg">
          <div {...getRootProps()}>
            <input {...getInputProps()} />
            <p>Drag 'n' drop some files here or click to select files</p>
          </div>
        </section>
      )}
    </ImageDropzone>
  );
}
