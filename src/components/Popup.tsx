import { useEffect, useState } from "react";
import ErrorIcon from "./icons/ErrorIcon";
import InfoIcon from "./icons/InfoIcon";
import WarningIcon from "./icons/WarningIcon";

interface PopupProps {
  apiResponse: Array<{ tagId: string; tagName: string; probability: number }>;
  handleClose: () => void;
}

interface Disease {
  disease_risk: boolean | undefined;
  disease_type: string | undefined;
}

const diseaseDict = {
  DR: {
    name: "Diabetic Retinopathy",
    description:
      "Diabetic retinopathy is a diabetes complication that affects eyes. It's caused by damage to the blood vessels of the light-sensitive tissue at the back of the eye (retina).",
  },
  MH: {
    name: "Age-related Macular Degeneration",
    description:
      "Age-related macular degeneration (AMD) is an eye disease that may get worse over time. It’s the leading cause of severe, permanent vision loss in people over age 60. It happens when the small central portion of your retina, called the macula, wears down.",
  },
  ODC: {
    name: "Optic Disc Coloboma",
    description:
      "Optic disc coloboma is a congenital abnormality of the optic disc that is caused by failure of closure of the embryonic fissure.",
  },
  TSLN: {
    name: "Tilted Optic Disc",
    description: "A congenital abnormality of the optic disc.",
  },
  DN: {
    name: "Dysplastic Nerve",
    description: "A congenital abnormality of the optic disc.",
  },
  MYA: {
    name: "Myelinated Nerve",
    description: "A congenital abnormality of the optic disc.",
  },
  ARMD: {
    name: "Age-related Macular Degeneration",
    description:
      "Age-related macular degeneration (AMD) is an eye disease that may get worse over time. It’s the leading cause of severe, permanent vision loss in people over age 60. It happens when the small central portion of your retina, called the macula, wears down.",
  },
  BRVO: {
    name: "Branch Retinal Vein Occlusion",
    description:
      "A blockage of the small veins that carry blood away from the retina.",
  },
  ODP: {
    name: "Optic Disc Pit",
    description: "A congenital abnormality of the optic disc.",
  },
  ODE: {
    name: "Optic Disc Edema",
    description: "A congenital abnormality of the optic disc.",
  },
};

export default function Popup({ apiResponse, handleClose }: PopupProps) {
  const [disease, setDisease] = useState<Disease>();

  // Find out if the image contains a disease, none or is undefined
  useEffect(() => {
    console.log(apiResponse);
    // if apiResponse contains Disease_Risk in the list with a sufficient probability > 0.5
    const diseaseRiskTag = apiResponse.find(
      (tag) => tag.tagName === "Disease_Risk"
    );
    const noDiseaseTag = apiResponse.find(
      (tag) => tag.tagName === "No_Disease"
    );

    if (diseaseRiskTag && diseaseRiskTag.probability > 0.5) {
      // find 1st tag that is not Disease_Risk
      const diseaseType = apiResponse.find(
        (tag) => tag.tagName !== "Disease_Risk" && tag.tagName !== "No_Disease"
      );
      setDisease({
        disease_risk: true,
        disease_type: diseaseType?.tagName,
      });
      return;
    }

    // if it contains no_disease with probability > 0.5
    else if (noDiseaseTag && noDiseaseTag.probability > 0.5) {
      setDisease({
        disease_risk: false,
        disease_type: undefined,
      });
      return;
    } else {
      setDisease({
        disease_risk: undefined,
        disease_type: undefined,
      });
    }
  }, [apiResponse]);

  return (
    <div
      className="relative z-10"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      {/* background */}
      <div className="fixed inset-0 bg-gray-500 bg-opacity-75" />

      <div className="fixed inset-0 z-10 w-screen overflow-y-auto flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
          <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
            <div className="sm:flex sm:items-start">
              {/* round with icon inside */}
              {disease?.disease_risk === true && (
                <>
                  <ErrorIcon />
                  <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                    <h3
                      className="text-base font-semibold leading-6 text-gray-900"
                      id="modal-title"
                    >
                      Result from EyeDetector : You are at risk of&nbsp;
                      {
                        diseaseDict[
                          disease.disease_type as keyof typeof diseaseDict
                        ].name
                      }
                      &nbsp; at a probability of&nbsp;
                      {Number(
                        (
                          apiResponse.find(
                            (tag) => tag.tagName === "Disease_Risk"
                          )?.probability ?? 0
                        ).toFixed(2)
                      ) *
                        100 +
                        "%"}
                    </h3>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500">
                        {
                          diseaseDict[
                            disease.disease_type as keyof typeof diseaseDict
                          ].description
                        }
                      </p>
                    </div>
                  </div>
                </>
              )}

              {disease?.disease_risk === false && (
                <>
                  <InfoIcon />
                  <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                    <h3
                      className="text-base font-semibold leading-6 text-gray-900"
                      id="modal-title"
                    >
                      Result from EyeDetector : You don't have any disease
                    </h3>

                    <div className="mt-2">
                      <p className="text-sm text-gray-500">
                        You are not at risk of any disease.
                      </p>

                      <p className="text-sm text-gray-500">
                        However, if you have any concerns, please consult your
                        doctor.
                      </p>
                    </div>
                  </div>
                </>
              )}

              {disease?.disease_risk === undefined && (
                <>
                  <WarningIcon />
                  <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                    <h3
                      className="text-base font-semibold leading-6 text-gray-900"
                      id="modal-title"
                    >
                      Result from EyeDetector : No result found
                    </h3>
                    <div className="mt-2">
                      <p className="text-sm text-gray-500">
                        No result found. Please verify that the image is clear
                        or try another image.
                      </p>
                    </div>
                  </div>
                </>
              )}
            </div>
          </div>
          <div className="bg-gray-100 px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
            <button
              type="button"
              className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
              onClick={handleClose} // add onClick event handler to close modal
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
